# Changelog — manuscript v1.2 (24 November 2026)

Supersedes v1.1 (19 November 2026). Artifact: v1.6.3, concept DOI 10.5281/zenodo.23920505.

## Corrections to claims

1. **"0/10,000 under the gate" removed.** No run-level zero is presented as a gated result. The only gated denominator is 30,798. The two 10,000-record runs with zero false successes contain 4,167 gated records each and their zero applies to the whole run (§4.5).
2. **"36,550 under the gate" remains withdrawn** and is now explained in the dataset README as a fact about the archive rather than a note to the authors (§4.5, LUMI_RAW_README.md).
3. **No rate over the 12,344-record chained set.** The set is integrity-only; §3.1 says so explicitly, which removes the 0.43% figure and the probe-mix denominator problem.
4. **`0.43%`, `918 probes`, `53 false successes`**: absent from the manuscript.

## New analysis

5. **Case-level gate comparison (Table 4.2).** The gate is a property of the case type within a run: `mp03`, `mp04`, `mp05`, `mp06`, `mp12` gated; `mp01`, `mp02`, `mp07`–`mp11` not. The five gated case types give 5,495 false successes in 11,353 ungated records (48.4%) against 0 in 30,798 gated records; the seven never-gated case types give 201 in 58,989 (0.34%).
6. **Matched 10,000-record pair (Table 4.3).** `lumi-20261104-011605` (gate off) 1,683 false successes vs `lumi-20261104-020310` (gate on) 0 — same model (Qwen2.5-7B), same day, identical `prompt_sha` for all twelve case types.
7. **§5.5 rewritten** as "Gate assignment, case composition and what the comparison supports": case composition is controlled, run-level factors are not, no effect size is estimated, a paired on/off run is named as planned work.
8. **Full run inventory.** All 24 runs with records, gated count, false successes and model (Appendix A.2); gate on/off by case type (Appendix A.3).

## Precision and framing

9. **Mistral runs explained** (§4.5): 168 gated → 0 FS, 232 unguarded → 198 FS; `false_note` = `contains` 96 / `exact` 68 / `refuse` 34; answer-check failures, excluded from cross-model statements.
10. **MockLiar labelled as simulated** (§4.6), with an explicit statement that 400/400 is not a sensitivity estimate for unconstrained agents.
11. **Aggregate-only material** (6,900-item corpus, 50-task x 6-model audit) declared in §1.3, §6 item 11 and Appendix A.
12. **Provenance and licences** (§3.1, §6 item 10, `LICENSES_AND_OUTPUTS.md`): synthetic prompts, no personal data (six placeholder e-mail strings, zero ID numbers), per-model licence terms, hash-and-length variant available.
13. **Ethics and corresponding author** filled in Appendix B.

## Identifiers and reproducibility

14. **Artifact cited as v1.6.3 with the concept DOI** 10.5281/zenodo.23920505; v1.6.2 (10.5281/zenodo.24378026) and v1.6.0 (10.5281/zenodo.24369933) listed as previous versions. Data-file digests unchanged.
15. **`recount.py` extended**: `--trust2` covers the 4-node sibling, and `--lumi` now prints per-run (with model) and per-case breakdowns, so the appendix tables are reproducible with one command.
16. **`recount_output.json` regenerated** from all five files: honest 25,600/0, liar 28,800/400, trust 25,600/1,600, trust2 19,200/1,200, lumi 101,140 / gated 30,798 / FS 5,696 / FS-gated 0.

## Documentation

17. **`LUMI_RAW_README.md` rewritten in English** for the artifact and mirrored to `dataset/lumi/raw/README.md`: run table with a gated column, per-case table, mapping to the numbers used in the paper, no internal notes.
18. **`LICENSES_AND_OUTPUTS.md` added** to the artifact.
19. **`RESPONSE_TO_REVIEW.md`** added: point-by-point answer with the recount command for each number.
