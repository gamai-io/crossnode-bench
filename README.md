[![CI](https://github.com/gamai-io/crossnode-bench/actions/workflows/ci.yml/badge.svg)](https://github.com/gamai-io/crossnode-bench/actions/workflows/ci.yml)

# CrossNode-Bench

**Most agent benchmarks score the final text. CrossNode-Bench scores the claim against ground truth on each node.**

If a node returns `ok:true` after a timeout, an action that never happened, or a GUI that never opened,
that record is counted as **false success**, not a pass. On a heterogeneous fleet this is the failure
mode that matters: the agent says "done", the user believes it, and nothing changed on the target machine.

## What it measures

- **pass rate** — the claim matched independent ground truth
- **false-success rate** — claimed success, independently verified as failure
- **by kind** — `read`, `action`, `cross`, `probe`
- **latency** — p50 / p95 per task
- **evidence** — one JSONL record per task with command hash, output hash, rc, verdict and reason

Each run writes `runs/<timestamp>/evidence.jsonl`, `report.json` and `REPORT.md`
(the report includes the SHA-256 of the evidence payload).

## Quickstart

No dependencies, Python 3.10+.

```bash
python3 crossnode.py --demo
```

Demo output on a clean machine:

```json
{
  "records": 48,
  "passed": 46,
  "false_success": 2,
  "pass_rate": 0.9583,
  "false_success_rate": 0.0417,
  "latency_ms": {"p50": 3.2, "p95": 31.3}
}
```

The two false successes are intentional: the demo wraps two nodes in `MockLiar`, which claims
`ok:true` for a missing program and a missing app. The benchmark detects both.

## Real fleet

```bash
cp examples/nodes.json nodes.json
# edit urls + token env vars
python3 crossnode.py --config nodes.json --runs 3
```

Node adapters:

| adapter | what it does |
|---|---|
| `LocalNode` | runs commands on this machine (demo / CI) |
| `HTTPNode` | `POST {"cmd": "..."}` to any JSON endpoint, token header |
| `MockLiar` | wraps a node and lies on selected probes (demonstrates detection) |

The HTTP adapter is intentionally transport-agnostic: SSH wrappers, Windows agents,
Android bridges and container executors all fit behind one `POST {"cmd": ...}` contract.

## Tasks (16)

- 6 read-only probes (identity, kernel, arithmetic, stdout fidelity, file write, hash read)
- 4 action probes (create, copy, read back, exact delete)
- 4 cross-node consistency probes (hash compare, non-empty, byte count, equality)
- 2 negative probes (missing program, missing app) — the claim-vs-truth checks

A pass requires both the node's claim and the independent verifier to agree.

## How a verdict is produced

```
claim_ok  = node said it succeeded (ok / rc)
truth_ok  = independent check (output, file, hash, exit code) agrees
passed    = claim_ok and truth_ok
false_success = claim_ok and not truth_ok
```

## Limits (read this)

- The demo uses a local shell. It measures the harness logic, not a remote OS.
- `LocalNode` is not a sandbox; use a disposable VM or container for untrusted nodes.
- The two negative probes only detect the configurations they target. Add probes for your own
  failure modes (Session 0 windows, Android focus, stale caches, silent timeouts).
- This is a measurement tool. It does not make an agent honest; it makes dishonesty visible.

## License

Apache-2.0.


## Validation — LUMI-C large-N (2026-11-01)

Run on LUMI-C (4 heterogeneous CPU nodes, ~0 GPU-h): **16 tasks × 4 nodes × 300 runs = 19,200 claim-vs-truth trials**.

| metric | value |
|---|---|
| trials | 19,200 |
| pass rate | 93.75% |
| false-success rate | 6.25% (1,200 — every dishonest claim flagged) |
| read / action / cross false-success | 0 / 0 / 0 |
| latency | p50 2.4 ms · p95 10.8 ms |

Reproduce: `NODES=4 RUNS=300 ./repro-lumi.sh f2` (EHPC `eurohpc-project`, `small` partition allows max 4 nodes; use `--partition=standard` for more nodes).
