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
lumi/aggregate.json                  1,000 raw + 10,000 guarded aggregate
```

## Reproduce
- Cross-node: https://github.com/gamai-io/crossnode-bench (`crossnode.py`, `SPEC.md`)
- Guard: https://github.com/gamai-io/gamai-guard (`bench/eval_blind.py`)
- LUMI: https://github.com/renatoschust-dot/gama-lumi-bench
- Claim verification / receipts: https://github.com/gamai-io/proofgate-runtime

## Caveats
- The 25,600 run is a **controlled detection-recall test**, not a field rate.
- The guard blind set is **40 items, self-authored**; 96.7% is a baseline.
- LUMI guard v3 rerun is **1/10,000 (0.01%) — FAIL**, not zero. The earlier 0/10k was not reproduced.
- No independent security audit.

## License
Apache-2.0. Guard corpus extracted from `gamai-io/gamai-guard` (Apache-2.0); LUMI prompts from `gama-lumi-bench` (Apache-2.0).
