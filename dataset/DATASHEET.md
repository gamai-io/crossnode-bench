# Datasheet — gamAI evidence benchmark pack v0.1.0

## Identity
- **Name:** gamAI evidence benchmark pack
- **Version:** 0.1.0 (2026-11-05)
- **Maintainer:** Renato Schuster, GAMA/gamAI, Usora, Bosnia and Herzegovina
- **Repository:** https://github.com/gamai-io/crossnode-bench
- **Code DOI:** https://doi.org/10.5281/zenodo.23933835
- **License:** Apache-2.0 (code and included data)
- **Contact:** research@example.org

## Motivation
The pack supports reproducible evaluation of two failure modes in tool-using AI agents:
1. **False success** — an agent claims an action succeeded when the observed state says otherwise.
2. **Prompt injection** — untrusted text tries to override instructions or exfiltrate secrets.

It is a measurement pack, not a training corpus.

## What is included

| Path | Content | Instances |
|---|---|---|
| `crossnode/tasks.json` | 16 cross-node task definitions (read, action, cross, probe) | 16 |
| `crossnode/aggregate.json` | Aggregate results of the controlled 8-node run | 25,600 trials (aggregate only) |
| `guard/blind_multilingual.jsonl` | Blind multilingual prompt-injection/benign corpus (DE/FR/ES/BS) | 40 |
| `guard/blind_multilingual_results.json` | Per-layer results for the blind set | 40 |
| `guard/aggregate.json` | Aggregate blind-set + generated-corpus results | 40 + 6,900 (aggregate only) |
| `lumi/prompts_v2.json` | LUMI evaluation prompts | 110 prompts |
| `lumi/results.schema.json` | Result schema for LUMI runs | schema |
| `lumi/aggregate.json` | Raw and guarded false-success summary | 1,000 + 10,000 samples (12 prompt templates × ~833) |
| `vultr/aggregate.json` | Real multi-region Vultr fleet, 200 rounds | 25,600 honest + 28,800 liar (aggregate only) |
| `vultr/VULTR_2026-11-09.md` | Fleet summary and caveats | text |

## What is NOT included
- **Raw per-trial logs for the 25,600 cross-node trials.** Only the aggregate and task manifest are included.
- **The 6,900-item generated guard corpus.** Only aggregate results are included.
- **Raw 10,000 LUMI result records.** Only prompts, schema and aggregate results are included.
- **The 10,000 LUMI samples are 12 prompt templates repeated ~833 times**, not 10,000 distinct tasks. The templates are in `gama-lumi-bench/bench_v2/prompts_v1.json` (Apache-2.0).
- **Any industrial invoice/ERP data.** The Floor Copilot case study is separate and anonymized; no customer data is in this pack.

If you need raw logs for independent re-analysis, contact the maintainer. Do not assume the aggregate can be re-derived from the included files alone.

## Raw evidence inventory (what can be recounted independently)

Only the rows marked **yes** have raw per-trial JSONL in the public artifact; every other
number is aggregate-only and must not be described as recountable.

| Experiment | Raw JSONL | Where | Records |
|---|---|---|---|
| Cross-node runs (36 runs, 6/8 nodes), incl. 918 probes and 53 false successes | **yes** | `dataset/evidence_chained.jsonl.gz` (repo) and `evidence_chained.jsonl` (Zenodo), SHA-256 chain + Merkle root | 12,344 |
| Real 9-node Vultr fleet, honest | **yes** | `results/vultr-fleet-2026-11-09-200/honest/evidence.jsonl.gz`; Zenodo `vultr_honest_evidence.jsonl.gz` | 25,600 |
| Real 9-node Vultr fleet, controlled liar (`MockLiar`) | **yes** | `results/vultr-fleet-2026-11-09-200/liar/evidence.jsonl.gz`; Zenodo `vultr_liar_evidence.jsonl.gz` | 28,800 (400 FS) |
| LUMI E1 36,550 guarded requests and the 10,000-request concurrent run | **no** | aggregate only (`dataset/lumi/aggregate.json`) | — |
| LUMI 50-task × 6-model false-success audit | **no** | aggregate only | — |
| Prompt-injection guard, 6,900 generated corpus | **no** | aggregate only | — |
| Prompt-injection guard, 40-item blind set | **yes** (corpus + per-item results) | `dataset/guard/blind_multilingual.jsonl`, `blind_multilingual_results.json` | 40 |

Recount commands and expected outputs are in the root `EVIDENCE.md` and in
`dataset/RECOUNT.md`. The chain verifier (`tools/evidence.py`) is offline and does not
trust this repository: it recomputes every hash and the Merkle root from the records.

## Collection
- **Cross-node:** 8 nodes × 16 tasks × 200 runs = 25,600 controlled probes. A controlled share (6.25%) of probes carried deliberately dishonest claims; the evidence gate flagged them. Read/action/cross tasks produced 0 false successes.
- **Guard blind set:** 40 items authored for this check (30 attacks in DE/FR/ES/BS, 10 benign). Lexical-only blocked 4/30; lexical + bge-m3 blocked 29/30 with 0/10 false positives; one German wording missed.
- **LUMI:** raw model false-success 197/1,000 (19.7%); guard v3 10k rerun produced 1/10,000 (0.01%) and **failed** the zero target. The 10k run uses 12 prompt templates (~833 repetitions each), not 10,000 distinct tasks. The earlier 0/10,000 was not reproduced.
- **Vultr fleet:** 9 nodes (Contabo + 8 Vultr) × 16 tasks × 200 rounds = 25,600 honest records, 0 false success. The controlled liar run adds a `MockLiar` wrapper around one Vultr node: 28,800 records, 400 false successes (1.39%), all 400 flagged.

## Labeling and validation
- Cross-node ground truth is the observed system state (stdout, hash, exit code, file state), not the model's claim.
- The guard corpus labels are `attack` or `benign` by construction; the 40-item set is small and self-authored.
- No independent third-party audit has been performed on this pack.

## Intended uses
- Reproduce or compare false-success measurement.
- Evaluate an evidence gate or receipt layer.
- Evaluate prompt-injection detection on a small multilingual blind set.
- Teaching and student projects on agent reliability.

## Out-of-scope uses
- Do not use the aggregate as a field false-success rate.
- Do not treat the 40-item guard result as general multilingual performance.
- Do not use this pack to train a model to claim success; it is an evaluation pack.
- Do not infer vendor/model rankings from a controlled, self-authored test.

## Ethics and privacy
- No human-subject data.
- No personal data, credentials, tokens or customer records.
- The guard corpus contains synthetic attack strings; handle as untrusted text.
- The LUMI prompts are synthetic evaluation prompts.

## Maintenance
- Versioned with the repository; changes to tasks or labels require a new version.
- Issues: https://github.com/gamai-io/crossnode-bench/issues
- Citation: see `CITATION.cff`.

## Citation
If you use this pack, cite the repository and the code DOI above. For the preprint, cite `paper/preprint.pdf`.
