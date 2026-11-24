# Licences, model outputs and prompt provenance

Applies to artifact v1.6.3 (concept DOI 10.5281/zenodo.23920505) and to the manuscript v1.2.

## What the archive contains

- `lumi_guard_model_101140.jsonl.gz` — 101,140 per-request records from the LUMI-G campaign, including a `text` field on model runs (the model's answer, 1–600 characters).
- `trust_evidence_25600.jsonl.gz`, `trust_evidence_19200.jsonl.gz` — controlled cross-node runs.
- `vultr_honest_evidence.jsonl.gz`, `vultr_liar_evidence.jsonl.gz` — Vultr fleet runs.
- `evidence_chained.jsonl` — 12,344 chained claim-versus-truth records.

## Prompts

All prompts are synthetic and were produced from task templates of the authors' own operational tooling. They contain:

- no customer or supplier records;
- no personal names, addresses or telephone numbers;
- no personal e-mail addresses — a scan of all 101,140 `text` fields returns six e-mail-shaped strings, all placeholders (`vase_kompanije_email@domena.com`, `vaša.e.posta@kompanija.com`, `vaša.kompanija@domena.co`, `@adresa.com`);
- no national identification numbers (0 matches for 13-digit patterns);
- internal schema identifiers retained verbatim (for example the database name `vp2026`), because they are part of the prompt text and removing them would invalidate `prompt_sha`.

The only apparent telephone matches in the scan are shell `PATH` strings.

## Model outputs

| Model | Runs in campaign | Licence | Redistribution in this archive |
|---|---|---|---|
| Qwen2.5-7B-Instruct | 17 run ids | Apache-2.0 | Raw `text` included under Apache-2.0. |
| Mistral-Small-3.2-24B-Instruct-2506 | 2 run ids (200 records each) | Apache-2.0 | Raw `text` included under Apache-2.0. |
| Llama-3.3-70B-Instruct | 5 run ids | Llama 3.3 Community License | Raw `text` included with attribution to Meta; outputs are **not** used to train, fine-tune or improve any other language model; the Llama licence notice is shipped with the artifact. |

If a venue, reviewer or institution requires that no Llama output text be redistributed, a variant of the LUMI file can be generated in which, for Llama runs, `text` is replaced by `text_sha256` and `text_len`. Every count in the manuscript is computed from `false_success`, `harness.guard`, `run_id` and `case` only, so the variant reproduces all reported numbers unchanged. The same construction applies to any other model on request.

No licence review by counsel has been performed. This file records the terms as declared by the model cards and the terms under which the authors redistribute the records; it is not a legal opinion.

## Code

The benchmark, the recount script and the verification tooling are Apache-2.0.
