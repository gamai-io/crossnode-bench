# Evidence benchmark pack (v0.1.0)

Small, reproducible measurement pack for two agent failure modes:

- **False success** — the agent claims success but the observed state disagrees.
- **Prompt injection** — untrusted text tries to override instructions or leak secrets.

Start with [`DATASHEET.md`](DATASHEET.md). It states exactly what is included and what is **not**.

## Contents
```
crossnode/tasks.json                 16 task definitions
crossnode/aggregate.json             25,600-trial aggregate (raw logs not included)
guard/blind_multilingual.jsonl       40-item blind corpus (DE/FR/ES/BS)
guard/blind_multilingual_results.json
guard/aggregate.json                 40-item + 6,900 generated-corpus aggregates
lumi/prompts_v2.json                 110 LUMI prompts
lumi/results.schema.json
lumi/aggregate.json                  1,000 raw + 10,000 guarded samples (12 templates × ~833)
vultr/aggregate.json                 real 9-node Vultr fleet, 200 rounds (honest + liar)
vultr/VULTR_2026-11-09.md            Vultr fleet summary and caveats
```

## Reproduce
- Cross-node: https://github.com/gamai-io/crossnode-bench (`crossnode.py`, `SPEC.md`)
- Guard: https://github.com/gamai-io/gamai-guard (`bench/eval_blind.py`)
- LUMI: https://github.com/renatoschust-dot/gama-lumi-bench (`bench_v2/prompts_v1.json` — 12 templates used in the 1k/10k runs; `prompts_v2.json` is a newer 110-prompt set)
- Vultr fleet: https://github.com/gamai-io/crossnode-bench/tree/main/results/vultr-fleet-2026-11-09-200
- Claim verification / receipts: https://github.com/gamai-io/proofgate-runtime

## Caveats
- The 25,600 run is a **controlled detection-recall test**, not a field rate.
- The guard blind set is **40 items, self-authored**; 96.7% is a baseline.
- LUMI guard v3 rerun is **1/10,000 (0.01%) — FAIL**, not zero; it uses 12 prompt templates (~833 repetitions each), not 10,000 distinct tasks. The earlier 0/10k was not reproduced.
- The Vultr liar run is a controlled `MockLiar` wrapper around a real node; it flagged **400/400** lying probe claims. It is a detection test, not a field rate.
- No independent security audit.

## License
Apache-2.0. Guard corpus extracted from `gamai-io/gamai-guard` (Apache-2.0); LUMI prompts from `gama-lumi-bench` (Apache-2.0).
