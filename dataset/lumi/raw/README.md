# LUMI-G raw records (E1 guard / model campaign)

Source: LUMI project 465003647, `/project/project_465003647/gama/out/`.
One JSON object per request: `run_id, i, case, mode, model, prompt_sha, status, ok, ms, ttft_ms, text_len, usage, false_success, false_note, harness`, plus `text` on model runs.
Pulled 2026-11-19; concatenated file `lumi_guard_model_101140.jsonl.gz`.

| run_id | records | false_success | models |
|---|---|---|---|
| `lumi-20261110-031936` | 10000 | 0 | Llama-3.3-70B-Instruct |
| `lumi-20261110-002049` | 10000 | 1 | qwen25-7b |
| `lumi-20261104-011605` | 10000 | 1683 | qwen25-7b |
| `lumi-20261103-151200` | 10000 | 2347 | qwen25-7b |
| `lumi-20261104-020310` | 10000 | 0 | qwen25-7b |
| `lumi-20261104-111050` | 10000 | 1 | qwen25-7b |
| `lumi-20261110-001254` | 5000 | 0 | qwen25-7b |
| `lumi-20261103-150654` | 5000 | 1153 | qwen25-7b |
| `lumi-20261110-004937` | 5000 | 0 | Llama-3.3-70B-Instruct |
| `lumi-20261110-000814` | 5000 | 0 | qwen25-7b |
| `lumi-20261110-002843` | 5000 | 0 | Llama-3.3-70B-Instruct |
| `lumi-20261110-001650` | 5000 | 0 | qwen25-7b |
| `lumi-20261110-003925` | 5000 | 0 | Llama-3.3-70B-Instruct |
| `lumi-20261104-013504` | 1000 | 7 | qwen25-7b |
| `lumi-20261104-014029` | 1000 | 1 | qwen25-7b |
| `lumi-20261109-235834` | 1000 | 0 | qwen25-7b |
| `lumi-20261103-145941` | 1000 | 197 | qwen25-7b |
| `lumi-20261104-015816` | 1000 | 0 | qwen25-7b |
| `lumi-20261103-145916` | 512 | 86 | qwen25-7b |
| `lumi-20261109-223741` | 200 | 99 | Mistral-Small-3.2-24B-Instruct-2506 |
| `lumi-20261109-233200` | 200 | 99 | Mistral-Small-3.2-24B-Instruct-2506 |
| `lumi-20261103-145858` | 128 | 22 | qwen25-7b |
| `lumi-20261109-232714` | 50 | 0 | qwen25-7b |
| `lumi-20261109-234858` | 50 | 0 | Llama-3.3-70B-Instruct |
| **total** | **101140** | **5696** | |

## Mapiranje na brojeve iz teksta (paznja)
- 10,000-request runs: `lumi-20261110-031936` (0 FS), `lumi-20261104-020310` (0 FS), `lumi-20261110-002049` (1 FS), `lumi-20261104-111050` (1 FS), `lumi-20261104-011605` (1,683 FS, raw model), `lumi-20261103-151200` (2,347 FS, raw model).
- **36,550 nije jedan run u arhivi.** Zbir svih LUMI guard/model zapisa je 101,140. Ako rad tvrdi 36,550, mora navesti tacne run_id-ove ili formulu zbira; inace je broj neobnovljiv iz arhive.
- 19.7% raw false-success (197/1,000) = `lumi-20261103-145941` (1,000 records, 197 FS).
- 1/10,000 = `lumi-20261110-002049` ili `lumi-20261104-111050`; 0/10,000 = `lumi-20261110-031936` i `lumi-20261104-020310`.

## Recount
```
python3 - <<'PY'
import gzip,json,collections
c=collections.Counter(); fs=collections.Counter()
for line in gzip.open('lumi_guard_model_101140.jsonl.gz','rt'):
    r=json.loads(line); c[r['run_id']]+=1; fs[r['run_id']]+=bool(r.get('false_success'))
print(sum(c.values()), sum(fs.values()))  # 101140 <FS>
PY
```
