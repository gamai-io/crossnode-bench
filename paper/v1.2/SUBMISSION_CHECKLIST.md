# Submission checklist — manuscript v1.2 / artifact v1.6.3

Everything marked **[done]** was produced and verified on 2026-11-24 in this directory.
Everything marked **[you]** needs your account or your decision.

## 1. Before sending

- [done] `MANUSCRIPT.md` v1.2 — all ten review points addressed, plus case-level analysis and provenance section.
- [done] `manuscript_v1.2.pdf` — rendered from `MANUSCRIPT.md` (pandoc + weasyprint), 13 pages, includes Figure 4.1.
- [done] `RESPONSE_TO_REVIEW.md` + `.pdf` — point-by-point answer with the recount command for each number.
- [done] `CHANGELOG_v1.2.md` — 19 numbered changes.
- [done] `EMAIL_v1.2.md` — cover message in English and Bosnian.
- [done] `EVIDENCE_LINKS.md` — claim → file → SHA-256 → command → expected output.
- [done] `recount.py` + `recount_output.json` — reproduces every number including the appendix tables (`--trust2`, per-run, per-case).
- [done] `LUMI_RAW_README.md` — English data description, no internal notes; also copied to `dataset/lumi/raw/README.md`.
- [done] `LICENSES_AND_OUTPUTS.md` — model licences, prompt provenance, PII scan result, hash-and-length variant.
- [done] Data-file SHA-256 verified against the manuscript table (5/5 match).
- [done] Latency figures verified from the recount (honest p50 64.8 / p95 325.1; liar p50 171.3 / p95 332.7).
- [you] Authors, affiliations and funding in Appendix B.
- [you] Decide whether the Llama text stays in the archive or a hash-only variant is published.

## 2. Artifact v1.6.3 (Zenodo) — **PUBLISHED 2026-11-24**

**Live:** v1.6.4 https://doi.org/10.5281/zenodo.24502948 (29 files) — adds `lumi_prompts_v1.json`, `LUMI_RUN_MANIFEST.json`, schema v1.1, `RELEASE_v1.6.4.md`; data files unchanged.
Previous: v1.6.3 https://doi.org/10.5281/zenodo.24502789. Concept DOI 10.5281/zenodo.23920505 always resolves to the latest.

Deposit on the **existing record**, "New version":

1. `dataset/lumi/raw/README.md` → upload as `LUMI_RAW_README.md` (replaces the file that carried the Bosnian notes).
2. `LICENSES_AND_OUTPUTS.md` → new file.
3. `.zenodo.json` → already updated (version 1.6.3, new description without 0.43% / 0/10,000 / 36,550).
4. Everything else unchanged; the data digests in the paper stay valid.
5. Publish, then confirm the new version DOI and keep citing the **concept DOI** `10.5281/zenodo.23920505`.

## 3. Preprint v1.2 — **PUBLISHED 2026-11-24**

**Live:** https://doi.org/10.5281/zenodo.24502881 (type Preprint, CC-BY-4.0, manuscript v1.2 + MANUSCRIPT.md + EVIDENCE_LINKS.md).

1. Upload `manuscript_v1.2.pdf` (+ optionally `MANUSCRIPT.md`).
2. Type: **Preprint**. Keep the same record as the earlier preprint so the version chain is visible.
3. Description: same summary as the paper abstract; list the two figures/tables of the case-level comparison.
4. Related identifier: `isSupplementedBy` → artifact concept DOI.

## 4. Repository

- [done] `dataset/lumi/raw/README.md`, `dataset/RECOUNT.md`, `dataset/DATASHEET.md`, `dataset/CITATION.cff`, `dataset/lumi/aggregate.json`, `dataset/lumi/LUMI_2026-11-04.md`, `.zenodo.json`, `README.md` updated.
- [done] `paper/v1.2/` added (manuscript, response, changelog, email, evidence links, licence note, figure).
- [done] committed and pushed: `a5129d6` (code/data commit `65fe3d6` still resolves — HTTP 200).
- [you] After the push, if the commit hash is no longer `65fe3d6`, tell me and I update §7, Appendix B and reference [1].

## 5. Sending

- Use `EMAIL_v1.2.md`. Attach `manuscript_v1.2_package.zip`.
- Nothing is sent automatically; the draft carries no claim of having been sent.

## What to say if asked about the two new findings

1. **Case-level comparison.** The gate follows case type, so the record-level split is descriptive. The same five case types give 5,495 false successes in 11,353 ungated records and none in 30,798 gated ones; a matched 10,000-record pair on the same model and day gives 1,683 against 0. Still quasi-experimental: no effect size, paired run planned.
2. **Provenance.** Synthetic prompts from our own task templates; six placeholder e-mail strings and no personal data in 101,140 text fields; licences declared per model; hash-and-length variant available.
