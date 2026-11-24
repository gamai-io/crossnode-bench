# Evidence links — claim by claim (v1.2)

All links are public. Counts verified 2026-11-24 with `recount.py` (see the one-command block below).

| # | Claim in the paper | File | SHA-256 | Recount | Expected |
|---|---|---|---|---|---|
| A | Vultr honest: 25,600 records, 9 nodes, 0 false successes, p50 64.8 ms / p95 325.1 ms | [vultr_honest_evidence.jsonl.gz](https://github.com/gamai-io/crossnode-bench/raw/main/results/vultr-fleet-2026-11-09-200/honest/evidence.jsonl.gz) | `960b6614…e87049` | `recount.py --honest` | `records=25600, false_success=0` |
| B | Vultr liar: 28,800 records, 10 nodes, 400 false successes (200 P1 + 200 P2), all on `vultr-lax-liar`, p50 171.3 / p95 332.7 | [vultr_liar_evidence.jsonl.gz](https://github.com/gamai-io/crossnode-bench/raw/main/results/vultr-fleet-2026-11-09-200/liar/evidence.jsonl.gz) | `37285159…789674` | `recount.py --liar` | `records=28800, false_success=400` |
| C | Controlled cross-node: 25,600 records, 24,000 claims, 1,600 false successes | [trust_evidence_25600.jsonl.gz](https://github.com/gamai-io/crossnode-bench/raw/main/dataset/lumi/raw/trust_evidence_25600.jsonl.gz) | `311dd0d0…a4788b` | `recount.py --trust` | `records=25600, claims=24000, false_success=1600` |
| C' | Sibling run: 19,200 records, 18,000 claims, 1,200 false successes | [trust_evidence_19200.jsonl.gz](https://github.com/gamai-io/crossnode-bench/raw/main/dataset/lumi/raw/trust_evidence_19200.jsonl.gz) | `296bca94…69446` | `recount.py --trust2` | `records=19200, claims=18000, false_success=1200` |
| D1 | LUMI-G record level: 101,140 records, 24 run ids; gated 30,798 with 0 false successes; unguarded 70,342 with 5,696 (8.10%) | [lumi_guard_model_101140.jsonl.gz](https://github.com/gamai-io/crossnode-bench/raw/main/dataset/lumi/raw/lumi_guard_model_101140.jsonl.gz) | `49f13727…3ada2` | `recount.py --lumi` | `n=101140, guard=30798, fs_guard=0, fs=5696` |
| D2 | LUMI-G case level: five gated case types 5,495/11,353 ungated (48.4%) vs 0/30,798 gated; seven never-gated types 201/58,989 (0.34%) | same file | `49f13727…3ada2` | `recount.py --lumi` → `per_case` | `mp03..mp06,mp12: off 5,495/11,353; on 0/30,798` |
| D3 | Matched 10,000-record pair, Qwen2.5-7B, same day, identical `prompt_sha`: `…011605` 1,683 FS vs `…020310` 0 | same file | `49f13727…3ada2` | `recount.py --lumi` → `per_run` | `lumi-20261104-011605.fs=1683, lumi-20261104-020310.fs=0` |
| E | Integrity: 12,344 records, SHA-256 chain + Merkle root `eda02d9c9cd4ff14d594d144c2d319bb3a3d1ea16569638238be14779da3d11d2d` | concept DOI → `evidence_chained.jsonl` | `e79a43f4…10b97e` | `python3 tools/evidence.py verify --in evidence_chained.jsonl --manifest manifest.json` | `{"ok": true, "records": 12344}` |

Integrity-only: E is used for integrity verification and no rate in the paper is computed over it.

## Permanent identifiers

- Artifact v1.6.3 (concept DOI, always latest): https://doi.org/10.5281/zenodo.23920505
- Previous versions: v1.6.2 https://doi.org/10.5281/zenodo.24378026 · v1.6.0 https://doi.org/10.5281/zenodo.24369933
- Repository commit: https://github.com/gamai-io/crossnode-bench/commit/65fe3d6
- LUMI per-run and per-case table: `dataset/lumi/raw/README.md` (mirrors `LUMI_RAW_README.md` in the artifact)
- Licences and output provenance: `LICENSES_AND_OUTPUTS.md`
- Recount guide: `dataset/RECOUNT.md`
- Raw-evidence inventory: `dataset/DATASHEET.md`

## One-command recount

```bash
curl -sLO https://github.com/gamai-io/crossnode-bench/raw/main/results/vultr-fleet-2026-11-09-200/honest/evidence.jsonl.gz
mv evidence.jsonl.gz vultr_honest_evidence.jsonl.gz
curl -sLO https://github.com/gamai-io/crossnode-bench/raw/main/results/vultr-fleet-2026-11-09-200/liar/evidence.jsonl.gz
mv evidence.jsonl.gz vultr_liar_evidence.jsonl.gz
curl -sLO https://github.com/gamai-io/crossnode-bench/raw/main/dataset/lumi/raw/trust_evidence_25600.jsonl.gz
curl -sLO https://github.com/gamai-io/crossnode-bench/raw/main/dataset/lumi/raw/trust_evidence_19200.jsonl.gz
curl -sLO https://github.com/gamai-io/crossnode-bench/raw/main/dataset/lumi/raw/lumi_guard_model_101140.jsonl.gz
python3 recount.py --honest vultr_honest_evidence.jsonl.gz --liar vultr_liar_evidence.jsonl.gz \
  --trust trust_evidence_25600.jsonl.gz --trust2 trust_evidence_19200.jsonl.gz \
  --lumi lumi_guard_model_101140.jsonl.gz
```

## Not in the quantitative analysis (aggregate-only)

- 6,900-item generated prompt-injection corpus — aggregate only, no per-record file.
- 50-task x 6-model false-success audit — aggregate only, no per-record file.

Declared in Section 1.3, Section 6 item 11 and the closing note of Appendix A.
