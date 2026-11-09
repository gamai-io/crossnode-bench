# Vultr cross-node fleet run — 2026-11-09

Real multi-region cross-node run of CrossNode-Bench: one Contabo host + 8 Vultr
`vc2-1c-1gb` instances (Ubuntu 24.04), each running a token-protected HTTP node
agent (`node_agent.py`, systemd `gama-node-agent`, port 8787, `X-Token`).

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

### Honest run — 9 nodes, 30 rounds
- records: **3,840**
- passed: **3,840 / 3,840 (100%)**
- false success: **0**
- latency: p50 **62.8 ms**, p95 **323.8 ms**
- report: `honest/REPORT.md`
- evidence: `honest/evidence.jsonl.gz` sha256 `e53a8782e69000b58dce0bf8072da785f906b4c643abcf64cca6b07498842d9b`

### Controlled liar run — 10 nodes (one MockLiar), 30 rounds
- records: **4,320**
- passed: **4,260 / 4,320 (98.61%)**
- false success: **60 (1.39%)**
- all 60 on `vultr-lax-liar`, tasks **P1** (missing program) and **P2** (missing app)
- latency: p50 **170.7 ms**, p95 **330.2 ms**
- report: `liar/REPORT.md`
- evidence: `liar/evidence.jsonl.gz` sha256 `9ceab548137969a894693e132a656d8344ec79efd3a4dd34a9ef045a7a57da4e`
- false-success records: `liar/false_success.jsonl`

The liar wrapper is a controlled simulation (`MockLiar`) around a real Vultr
node: it returns `ok:true` for probe commands while the underlying command
fails. The benchmark correctly flags every such claim.

## Reproduce

```bash
cd crossnode-bench
# nodes.json: local + 8 http nodes with token_env NODE_TOKEN
export NODE_TOKEN=<agent token>
python3 crossnode.py --config nodes.json --runs 30
```

Agent contract: `POST /rpc` with `{"cmd": "..."}` and header `X-Token`.

## Caveats

- Probes (P1/P2) run only on nodes that expose a `probe` attribute; honest
  `HTTPNode` entries skip them. The liar run adds a `MockLiar` wrapper so the
  probe path is exercised.
- The liar run is a controlled detection test, not a field false-success rate.
- IPs and instance IDs are ephemeral; the node list is a snapshot from 2026-11-09.
- This is a small pilot (8 Vultr nodes, 30 rounds), not the full 10k campaign.
- Cost: ~40 USD/month for the 8 nodes (~1.33 USD/day); Vultr credit expires 2026-12-01.
