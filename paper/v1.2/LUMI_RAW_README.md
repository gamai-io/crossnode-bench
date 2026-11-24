# LUMI-G raw records (E1 guard / model campaign)

Source: LUMI project 465003647, `/project/project_465003647/gama/out/`.
One JSON object per request: `run_id, i, case, mode, model, prompt_sha, status, ok, ms, ttft_ms, text_len, usage, false_success, false_note, harness`, plus `text` on model runs.
Pulled 2026-11-19; concatenated file `lumi_guard_model_101140.jsonl.gz`.

Total: **101,140 records, 24 run identifiers, 12 case types, 3 models.**

## Gate structure

`harness.guard` is a property of the **case type within a run**, not a per-record randomisation:

- gated case types: `mp03`, `mp04`, `mp05`, `mp06`, `mp12` (5 of 12)
- never-gated case types: `mp01`, `mp02`, `mp07`, `mp08`, `mp09`, `mp10`, `mp11` (7 of 12)
- 15 runs are fully gated in this sense (5/12 of each run's records are gated: 4,167 of 10,000; 2,084 of 5,000; 417 of 1,000; 84 of 200)
- 3 runs of 1,000 records armed the gate on a subset of the five (`lumi-20261104-013504`, `lumi-20261104-014029`, `lumi-20261104-015816`)
- 6 runs (26,640 records) ran entirely without the gate

## Runs

| run_id | records | gated | false_success | model |
|---|---|---|---|---|
| `lumi-20261103-145858` | 128 | 0 | 22 | Qwen2.5-7B |
| `lumi-20261103-145916` | 512 | 0 | 86 | Qwen2.5-7B |
| `lumi-20261103-145941` | 1,000 | 0 | 197 | Qwen2.5-7B |
| `lumi-20261103-150654` | 5,000 | 0 | 1,153 | Qwen2.5-7B |
| `lumi-20261103-151200` | 10,000 | 0 | 2,347 | Qwen2.5-7B |
| `lumi-20261104-011605` | 10,000 | 0 | 1,683 | Qwen2.5-7B |
| `lumi-20261104-013504` | 1,000 | 250 | 7 | Qwen2.5-7B |
| `lumi-20261104-014029` | 1,000 | 334 | 1 | Qwen2.5-7B |
| `lumi-20261104-015816` | 1,000 | 417 | 0 | Qwen2.5-7B |
| `lumi-20261104-020310` | 10,000 | 4,167 | 0 | Qwen2.5-7B |
| `lumi-20261104-111050` | 10,000 | 4,167 | 1 | Qwen2.5-7B |
| `lumi-20261109-223741` | 200 | 84 | 99 | Mistral-Small-3.2-24B-Instruct-2506 |
| `lumi-20261109-232714` | 50 | 20 | 0 | Qwen2.5-7B |
| `lumi-20261109-233200` | 200 | 84 | 99 | Mistral-Small-3.2-24B-Instruct-2506 |
| `lumi-20261109-234858` | 50 | 20 | 0 | Llama-3.3-70B-Instruct |
| `lumi-20261109-235834` | 1,000 | 417 | 0 | Qwen2.5-7B |
| `lumi-20261110-000814` | 5,000 | 2,084 | 0 | Qwen2.5-7B |
| `lumi-20261110-001254` | 5,000 | 2,084 | 0 | Qwen2.5-7B |
| `lumi-20261110-001650` | 5,000 | 2,084 | 0 | Qwen2.5-7B |
| `lumi-20261110-002049` | 10,000 | 4,167 | 1 | Qwen2.5-7B |
| `lumi-20261110-002843` | 5,000 | 2,084 | 0 | Llama-3.3-70B-Instruct |
| `lumi-20261110-003925` | 5,000 | 2,084 | 0 | Llama-3.3-70B-Instruct |
| `lumi-20261110-004937` | 5,000 | 2,084 | 0 | Llama-3.3-70B-Instruct |
| `lumi-20261110-031936` | 10,000 | 4,167 | 0 | Llama-3.3-70B-Instruct |
| **total** | **101,140** | **30,798** | **5,696** | |

## By case type

| case | gate on: records | gate on: FS | gate off: records | gate off: FS |
|---|---|---|---|---|
| `mp01` | 0 | 0 | 8,441 | 34 |
| `mp02` | 0 | 0 | 8,441 | 34 |
| `mp03` | 6,132 | 0 | 2,307 | 165 |
| `mp04` | 6,216 | 0 | 2,223 | 1,676 |
| `mp05` | 6,208 | 0 | 2,220 | 2,216 |
| `mp06` | 6,042 | 0 | 2,386 | 1,178 |
| `mp07` | 0 | 0 | 8,428 | 34 |
| `mp08` | 0 | 0 | 8,428 | 3 |
| `mp09` | 0 | 0 | 8,417 | 32 |
| `mp10` | 0 | 0 | 8,417 | 32 |
| `mp11` | 0 | 0 | 8,417 | 32 |
| `mp12` | 6,200 | 0 | 2,217 | 260 |
| **total** | **30,798** | **0** | **70,342** | **5,696** |

Five gated case types: 5,495 false successes in 11,353 ungated records (48.4%) against 0 in 30,798 gated records.
Matched pair, same model, same day, identical `prompt_sha` per case: `lumi-20261104-011605` (gate off) 1,683 false successes vs `lumi-20261104-020310` (gate on) 0, 10,000 records each.

## Mapping to numbers used in the manuscript

- `0/30,798` — all records with `harness.guard = true`, summed over the 24 runs. No smaller denominator is used in the paper.
- `5,696 / 70,342 = 8.10%` — all records with `harness.guard = false`.
- `5,495 / 11,353 = 48.4%` — the five gated case types only, records with `harness.guard = false`.
- `201 / 58,989 = 0.34%` — the seven never-gated case types.
- `1,683` vs `0` — `lumi-20261104-011605` and `lumi-20261104-020310`, both 10,000 records, Qwen2.5-7B, 4 November 2026, identical `prompt_sha` for every case.
- `197/1,000 (19.7%)` — `lumi-20261103-145941`, completely ungated run.
- The earlier figure "36,550 requests under the gate" appears in no version of the manuscript from v1.1 onward. It was not reproducible from the per-record `harness.guard` flags and was withdrawn; it is not replaced by any run-level number.

## Mistral runs

`lumi-20261109-223741` and `lumi-20261109-233200` (200 records each, 99 false successes each) are answer-check failures: `false_note` values are `contains` (96), `exact` (68) and `refuse` (34), and all false successes are in the seven never-gated case types. They are not tool-execution false successes and are excluded from cross-model statements in the manuscript.

## Recount

```python
import gzip, json, collections
n = fs = g = fsg = 0
per = collections.defaultdict(lambda: [0, 0, 0, 0])
for line in gzip.open('lumi_guard_model_101140.jsonl.gz', 'rt'):
    r = json.loads(line)
    guard = bool((r.get('harness') or {}).get('guard'))
    n += 1
    if guard: g += 1
    if r.get('false_success'):
        fs += 1
        if guard: fsg += 1
        per[r['run_id']][2] += 1
    per[r['run_id']][0] += 1
    per[r['run_id']][1] += guard
print(n, g, fs, fsg)   # 101140 30798 5696 0
```

`recount.py --lumi` prints the same totals plus the per-run and per-case breakdown used in Appendix A.

## Provenance and licences

Prompts are synthetic and derived from the authors' task templates; no customer records, names, addresses, telephone numbers or personal e-mail addresses are present. Internal schema identifiers (for example `vp2026`) are retained because they are part of the prompt text. See `LICENSES_AND_OUTPUTS.md` in the archive root for the model licences and the redistribution terms of the recorded outputs.
