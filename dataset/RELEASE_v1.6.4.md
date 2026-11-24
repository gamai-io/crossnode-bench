# Artifact v1.6.4 — what is new

Release date: 2026-11-24. Supersedes v1.6.3 (`10.5281/zenodo.24502789`). Concept DOI: `10.5281/zenodo.23920505`.

**Data files are unchanged.** All SHA-256 digests in the manuscript's table remain valid; this release adds recorded configuration and the missing test set.

## Added

| File | What it is |
|---|---|
| `lumi_prompts_v1.json` | The 12-case prompt set used by the LUMI-G campaign, with expected answer and check kind (`exact`, `number` + tolerance, `contains`, `refuse`, `honest`, `safe`). `sha256(prompt)` matches the `prompt_sha` field of every record set 12/12. |
| `LUMI_RUN_MANIFEST.json` | Per-run record: model, recorded model path, records, gated/ungated split, case types, repetitions per case, guard applied/version where documented, prompt-set hash, sampling parameters (temperature 0, seed 42), start/finish timestamps. |
| `results.schema.json` | Schema v1.1: adds optional `guard_version`, `guard_code_sha256`, `model_sha256`, `model_revision`, `tensor_parallel_size`, `max_num_seqs`, `temperature`, `seed`. Rows from the 2026-11 campaign remain valid because the fields are optional and absent there. |

## Still not available for the 2026-11 campaign

These were not captured at run time and cannot be reconstructed afterwards. They are listed in `LUMI_RUN_MANIFEST.json` under `not_recorded`:

- model weight digests (`model_sha256`);
- tensor-parallel degree and `max_num_seqs` per run;
- guard version per record (only the `harness.guard` boolean exists);
- guard implementation hash at run time.

The guard version is documented for the five 2026-11-04 runs (`v3`, see `LUMI_2026-11-04.md`); for the 2026-11-09/10 runs it is not recorded, and the manifest says so per run instead of guessing.

## Why this matters

The 101,140 records are **repetitions of 12 tasks**, not 101,140 independent tasks. The manifest now states that per run (`repetitions_per_case`), so the reproducibility claim cannot be misread as sample breadth.

## What this release does not change

- No reported number in manuscript v1.2 changes: totals, case-level comparison, matched pair, digests.
- No new experiments; nothing was re-run.
- The manuscript itself is a separate Preprint record: `10.5281/zenodo.24502881`.
