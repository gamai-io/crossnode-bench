# Vultr cross-node fleet — 200-round campaign (2026-11-09)

Same fleet as `results/vultr-fleet-2026-11-09/`: one Contabo host + 8 Vultr
`vc2-1c-1gb` instances (Ubuntu 24.04), each running a token-protected HTTP node
agent (`node_agent.py`, systemd `gama-node-agent`, port 8787, `X-Token`).
Runs: **200 rounds** per task.

## Nodes

| Node | Region | Provider |
|---|---|---|
| contabo | Frankfurt (local host) | Contabo |
| vultr-fra | Frankfurt | Vultr |
| vultr-ams | Amsterdam | Vultr |
| vultr-lhr | London | Vultr |
| vultr-mad | Madrid | Vultr |
| vultr-ewr | New Jersey | Vultr |
| vultr-ord | Chicago | Vultr |
| vultr-dfw | Dallas | Vultr |
| vultr-lax | Los Angeles | Vultr |

`gama-node-cdg` (Paris) failed provisioning/SSH and was deleted; it is not part of these runs.

## Results

### Honest run — 9 nodes, 200 rounds
- records: **25,600**
- passed: **25,600 / 25,600 (100%)**
- false success: **0**
- latency: p50 **64.8 ms**, p95 **325.1 ms**
- report: `honest/REPORT.md`
- evidence: `honest/evidence.jsonl.gz` sha256 `960b661424b2c2a147ad2179d15aeab357a34ce6e45b3e8564066fe824e87049`
- false-success records: `honest/false_success.jsonl` (0 lines)

### Controlled liar run — 10 nodes (one MockLiar), 200 rounds
- records: **28,800**
- passed: **28,400 / 28,800 (98.61%)**
- false success: **400 (1.39%)**
- all 400 on `vultr-lax-liar`, tasks **P1** (missing program) and **P2** (missing app)
- latency: p50 **171.3 ms**, p95 **332.7 ms**
- report: `liar/REPORT.md`
- evidence: `liar/evidence.jsonl.gz` sha256 `372851594aae1ee554a46b817a0c466fad3edda4f3e9a0ecff2df9a081789674`
- false-success records: `liar/false_success.jsonl` (400 lines)

The liar wrapper is a controlled simulation (`MockLiar`) around a real Vultr
node: it returns `ok:true` for probe commands while the underlying command
fails. The benchmark flags every such claim (400/400).

## Reproduce

```bash
cd crossnode-bench
# nodes.json: local + 8 http nodes with token_env NODE_TOKEN
export NODE_TOKEN=<agent token>
python3 crossnode.py --config nodes.json --runs 200
```

Agent contract: `POST /rpc` with `{"cmd": "..."}` and header `X-Token`.

## Caveats

- Probes (P1/P2) run only on nodes that expose a `probe` attribute; honest
  `HTTPNode` entries skip them. The liar run adds a `MockLiar` wrapper so the
  probe path is exercised.
- The liar run is a controlled detection test, not a field false-success rate.
- IPs and instance IDs are ephemeral; the node list is a snapshot from 2026-11-09.
- This is a pilot-scale campaign (9–10 nodes), not a production field study.
- Cost: ~40 USD/month for the 8 nodes (~1.33 USD/day); Vultr credit expires 2026-12-01.
