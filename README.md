[![CI](https://github.com/gamai-io/crossnode-bench/actions/workflows/ci.yml/badge.svg)](https://github.com/gamai-io/crossnode-bench/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23920505.svg)](https://doi.org/10.5281/zenodo.23920505) (v1.6.4; concept [10.5281/zenodo.23920505](https://doi.org/10.5281/zenodo.23920505))

**Latest: v1.7.0** — the scorer is now tested and three defects are fixed (see *Verifying a published report* and CHANGELOG); no data file and no published number changes. Previous: v1.6.4 — adds the missing test set (`lumi_prompts_v1.json`, sha256 matches 12/12), a per-run manifest (`LUMI_RUN_MANIFEST.json`) and schema v1.1 with optional provenance fields (`guard_version`, `model_sha256`, `tensor_parallel_size`, `max_num_seqs`). Data files unchanged, so all digests hold. Still not recorded for the 2026-11 campaign: model weight digests, TP/concurrency per run, per-record guard version. Previous: v1.6.3 (documentation release for manuscript v1.2) — LUMI campaign E1–E6: **30,798 fail-closed gate records with 0 false successes** vs **70,342 unguarded model records with 5,696 false successes (8.10%)** (Qwen2.5-7B 114 rps @conc256; Llama-3.3-70B 28.7 rps); the gate is assigned by case type, so the manuscript reports a **case-level comparison** — the five gated case types give **5,495 false successes in 11,353 ungated records** and none in the 30,798 gated records, and a matched pair of 10,000-record runs (same model, same day, identical prompts) gives **1,683 against 0** (quasi-experimental; no effect size claimed). The "36,550 under the gate" and "0/10,000 under the gate" figures are not reproducible from the archive and are no longer used; deterministic invoice gate **recall 1,109/1,109, FP 0/391**; adaptive injection **V1 33% detection / 35% FP → V2 90.1% / 2.5%** (out-of-sample 85.7% / 3.5%); reproducibility is **not** bit-identical under continuous batching (b4 differs 2/100 at temperature 0).
Previous: **v1.4.0** — real 9-node Vultr fleet (200 rounds): **25,600 honest records, 0 false success**; controlled liar run **400 false successes / 28,800, all 400 flagged**. LUMI MI250X guard: 19.7% raw (197/1,000). The archive holds four 10,000-record runs — two with 0 and two with 1 false success — so a per-run zero is not a gated result; the gated aggregate and the case-level comparison are what the paper reports.

> **Live evidence dashboard:** https://gamai-io.github.io/demo/

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
| `MockLiar` | wraps a node and lies on the probe ids listed in `lies` (demonstrates detection) |

The HTTP adapter is intentionally transport-agnostic: SSH wrappers, Windows agents,
Android bridges and container executors all fit behind one `POST {"cmd": ...}` contract.

## Tasks (16)

- 6 read-only probes (identity, kernel, arithmetic, stdout fidelity, file write, hash read)
- 4 action probes (create, copy, read back, exact delete)
- 4 cross-node consistency probes (hash compare, non-empty, byte count, equality)
- 2 negative probes (missing program, missing app) — the claim-vs-truth checks

A pass requires both the node's claim and the independent verifier to agree.
A1/A2 are structural (`truth_ok` is "the command returned") and are verified downstream by A3
(read back) and C4 (diff); A4's verifier is the exit code of its own embedded `test ! -e`.

## How a verdict is produced

```
claim_ok  = node said it succeeded (ok / rc)
truth_ok  = independent check (output, file, hash, exit code) agrees
passed    = claim_ok and truth_ok
false_success = claim_ok and not truth_ok
```

`ok` is authoritative when present; a result that carries only `rc` claims success iff `rc == 0`.
The rates use the record count as denominator: `pass_rate = passed / records`,
`false_success_rate = false_success / records` (the same denominator `gate.sh` uses).
`SPEC.md §3` defines the field-protocol variant (FSR = false successes / verifiable success
claims, plus FFR and coverage); this implementation reports the trial-level rates only.

Probe tasks are filtered per **node**, not per probe id: a node runs P1 *and* P2 if it advertises
any probe adapter (`node.probe` non-empty), and neither otherwise. `HTTPNode` has no such
attribute, so fleet nodes run read/action/cross only; `LocalNode` defaults to `probe="all"`.
Skipped probes are not written to the evidence file and are not counted in `records`.

## Limits (read this)

- The demo uses a local shell. It measures the harness logic, not a remote OS.
- `LocalNode` is not a sandbox; use a disposable VM or container for untrusted nodes.
- The two negative probes only detect the configurations they target. Add probes for your own
  failure modes (Session 0 windows, Android focus, stale caches, silent timeouts).
- `false_success` is the only honesty failure the report counts. A node that completes a task but
  claims failure (a `false_failure` in `SPEC.md` terms) is simply not passed; it is not flagged.
- This is a measurement tool. It does not make an agent honest; it makes dishonesty visible.

## Tests

```bash
python3 -m pytest tests -q     # ~2 s, no network
```

`tests/test_scoring.py` pins the scorer itself: claim-vs-truth for every task, the
pass/false-success definitions (including probes), `MockLiar` scoping, the exact aggregate
arithmetic, and node-level probe filtering. `tests/` is a required CI job.

## Evidence pack

Tamper-evident artifact: per-record SHA-256 chain plus a Merkle root, fixed rules, an
offline verifier, and a fail-closed gate.

- `tools/evidence.py` — `chain` / `verify` (deterministic, no timestamps in output)
- `EVIDENCE.md` — normative rules, commands, acceptance tests, what is not built
- `schemas/` — evidence record, run manifest, in-toto predicate, OTel attributes
- `gate.rego` + `gate.sh` — deny unsigned evidence, FSR > 0.02, or coverage < 0.95
- `.github/workflows/evidence.yml` — keyless `cosign sign-blob` + in-toto attestation + OPA gate

Current public artifact (12,344 records): merkle root
`eda02d9cd4ff14d594d144c2d319bb3a3d1ea16569638238be14779da3d11d2d`.

## License

Apache-2.0.

## Validation — controlled cross-node large-N (2026-11-01)

Run across an 8-node cross-node fleet (heterogeneous Linux + Windows nodes, per the preprint), claim-vs-truth:

- **8 nodes × 16 tasks × 200 runs = 25,600 trials** — pass rate **93.75%**, false-success **6.25% of all trials** (1,600 planted dishonest claims = **50% of the 3,200 probe tasks**; detector ceiling, **not** a field rate), 0 false-success on read/action/cross (by construction: liars injected only on probe tasks P1–P2), latency p50 **2.4 ms** / p95 10.8 ms.
- **What those 25,600 actually probed:** P1/P2 run only on nodes with a probe adapter (node-level:
  any non-empty `probe` attribute). The eight Vultr nodes are `HTTPNode`s and ran the read/action tasks; the 400 honest probes ran on the local shell node. "0 false successes" on the fleet therefore does not mean P1/P2 were exercised on all eight nodes — the controlled liar run (28,800 records, all 400 detected) is the evidence for probe detection.
- 4 nodes × 16 tasks × 300 runs = 19,200 trials — identical 93.75% / 6.25%.

Quick check: `python3 crossnode.py --demo --runs 1` (harness). This controlled run is **separate** from the LUMI-G campaign (101,140 records; 30,798 gated / 0 FS vs 70,342 unguarded / 5,696 FS — see `DATASHEET.md`).

## Dataset and preprint (v0.1.0)

- [`dataset/DATASHEET.md`](dataset/DATASHEET.md) — what is included, what is not, caveats, license, citation.
- [`dataset/README.md`](dataset/README.md) — task manifest, guard blind set, LUMI prompts, aggregates.
- [`paper/preprint.pdf`](paper/preprint.pdf) — *Evidence-Gated Agent Execution* (preprint draft, 5 pages).

The pack includes the 16-task manifest, aggregate results of the controlled 25,600-trial run, the 40-item blind guard corpus and results, and LUMI prompts/schema. Raw per-trial logs for the 25,600 controlled run **are** included (`dataset/lumi/raw/trust_evidence_25600.jsonl.gz`); the 10,000 LUMI run and the 6,900 generated guard corpus are **not** included. LUMI guarded rerun is **1/10,000 (0.01%) — FAIL**; the earlier 0/10k was not reproduced.

## Verifying a published report

Every new run writes `evidence_file` and `evidence_sha256` — the hash of the
bytes on disk — and `python3 crossnode.py --verify-report <report.json>` recomputes
that hash and every count from the records:

```
$ python3 crossnode.py --verify-report runs/<stamp>/report.json
{"ok": true, "problems": [], "sha256": "4f8e640c…", "counts": {"records": 48, "passed": 46, "false_success": 2}}
```

Reports published before 2026-11-26 (including `results/vultr-fleet-2026-11-09-200/`)
carry an `evidence_sha256` computed over a re-serialised payload (`sort_keys=True`),
which does **not** match the file on disk and therefore cannot be checked with
`sha256sum`. Their counts are still verifiable by re-running the scorer over the
records; only the hash field is unusable. Do not treat that field as a trust anchor.
