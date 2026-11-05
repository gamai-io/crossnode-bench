# v1.3.0 — evidence benchmark pack + preprint

This release packages the measurement artifacts behind the false-success and prompt-injection claims.

## Included
- `dataset/crossnode/tasks.json` — 16 task definitions.
- `dataset/crossnode/aggregate.json` — 25,600-trial controlled aggregate.
- `dataset/guard/blind_multilingual.jsonl` — 40-item blind multilingual corpus.
- `dataset/guard/blind_multilingual_results.json` + `aggregate.json`.
- `dataset/lumi/prompts_v2.json` + `results.schema.json` + `aggregate.json`.
- `dataset/DATASHEET.md`, `dataset/README.md`, `dataset/SHA256SUMS`, `dataset/CITATION.cff`.
- `paper/preprint.pdf` — preprint draft (5 pages).

## Not included
- Raw per-trial logs for the 25,600 cross-node run.
- The 6,900-item generated guard corpus.
- Raw 10,000 LUMI result records.

## Caveats
- 25,600 is a controlled detection-recall test, not a field false-success rate.
- The guard blind set is 40 items and self-authored; 96.7% is a baseline.
- LUMI guarded rerun is 1/10,000 (0.01%) — FAIL; earlier 0/10k was not reproduced.
- No independent audit; preprint is not peer reviewed.

License: Apache-2.0. Code DOI: https://doi.org/10.5281/zenodo.23933835
