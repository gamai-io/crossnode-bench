# Recount guide — CrossNode-Bench artifact v1.6.3

Concept DOI (always latest): https://doi.org/10.5281/zenodo.23920505
Previous version used by manuscript v1.1: v1.6.2, https://doi.org/10.5281/zenodo.24378026

Everything below uses Python 3 standard library only. No model, GPU, network or cluster is required.

## Files

| File | What it is | SHA-256 |
|---|---|---|
| `evidence_chained.jsonl` | 12,344 chained claim-vs-truth records (integrity set) | `e79a43f4a51ee94fb70a8f82eca7e01e71ebc6b5766aa898b93a8cd6ee10b97e` |
| `manifest.json` | chain manifest (records, merkle_root) | `a84642af61634ff70745f36c6f9483b2588e89987a954b5910d1d660cc884df8` |
| `vultr_honest_evidence.jsonl.gz` | 9-node Vultr fleet, 25,600 records, 0 false successes | `960b661424b2c2a147ad2179d15aeab357a34ce6e45b3e8564066fe824e87049` |
| `vultr_liar_evidence.jsonl.gz` | controlled liar run, 28,800 records, 400 false successes | `372851594aae1ee554a46b817a0c466fad3edda4f3e9a0ecff2df9a081789674` |
| `trust_evidence_25600.jsonl.gz` | controlled cross-node run, 25,600 records, 1,600 false successes | `311dd0d0ddfa52c1bc00a3407d4aa5cb4d17e2830c5509f435b5ed52d0a4788b` |
| `trust_evidence_19200.jsonl.gz` | sibling run, 19,200 records, 1,200 false successes | `296bca949625383454a4bc874b9eeefc45f38e4372c42fdea3ad9e66334e9446` |
| `lumi_guard_model_101140.jsonl.gz` | LUMI-G campaign, 101,140 records, 24 run ids | `49f13727c1ba1effa1d941b82be23d33c6665407e881a580486bb2cd7263ada2` |

## One command for the manuscript numbers

```bash
python3 recount.py --honest vultr_honest_evidence.jsonl.gz \
                   --liar   vultr_liar_evidence.jsonl.gz \
                   --trust  trust_evidence_25600.jsonl.gz \
                   --trust2 trust_evidence_19200.jsonl.gz \
                   --lumi   lumi_guard_model_101140.jsonl.gz
```

Expected: `honest 25600/0`, `liar 28800/400`, `trust_25600 25600/1600`, `trust_19200 19200/1200`, `lumi n=101140 guard=30798 fs=5696 fs_guard=0`, plus per-run and per-case breakdowns.

## Independent checks without our code

```python
# integrity chain + Merkle root
# expected: {"merkle_root":"eda02d9c...d11d2d","ok":true,"records":12344}
python3 tools/evidence.py verify --in evidence_chained.jsonl --manifest manifest.json

# counts in the chained set
# expected: 12344 11206 53
python3 - <<'PY'
import json
n = claims = fs = 0
for line in open('evidence_chained.jsonl'):
    r = json.loads(line); n += 1
    if r.get('claim_ok'): claims += 1
    if r.get('claim_ok') and r.get('truth_ok') is False: fs += 1
print(n, claims, fs)
PY

# LUMI-G totals
# expected: 101140 30798 5696 0
python3 - <<'PY'
import gzip, json
n = g = fs = fsg = 0
for line in gzip.open('lumi_guard_model_101140.jsonl.gz', 'rt'):
    r = json.loads(line); guard = bool((r.get('harness') or {}).get('guard'))
    n += 1; g += guard
    if r.get('false_success'):
        fs += 1; fsg += guard
print(n, g, fs, fsg)
PY
```

## A note on the 53 false successes in the chained set

They are a count inside the 918 probe records of that set. The manuscript reports **no percentage** over the 12,344 records, because a ratio over the full set would mix probe and non-probe records; the chained set is used for integrity verification only.

## Gate structure in the LUMI-G file

`harness.guard` follows the case type within a run: `mp03`, `mp04`, `mp05`, `mp06`, `mp12` are gated; `mp01`, `mp02` and `mp07`–`mp11` never are. 15 runs are fully gated in this sense, three 1,000-record runs armed the gate on a subset, and six runs (26,640 records) ran entirely without it. See `lumi/raw/README.md` for the run table and the per-case table.

## Not in the quantitative analysis

- 6,900-item generated prompt-injection corpus — aggregate only, no per-record file.
- 50-task x 6-model false-success audit — aggregate only, no per-record file.
