# Response to review — manuscript v1.2

**Manuscript:** Evidence-Gated Verification of Tool-Using Agent Execution Across a Heterogeneous Multi-Region Fleet
**Version:** v1.2 (supersedes v1.1 of 19 November 2026)
**Date:** 24 November 2026
**Artifact:** v1.6.3, concept DOI 10.5281/zenodo.23920505

Every number below is printed by `recount.py` from the published files; the command is given with each item. Comments are reproduced in short form, followed by the change and where it is visible in v1.2.

---

## 1. "0/10,000 is not reproducible from the raw table; two 10,000-record runs have 0 false successes, two have 1"

**Agreed — and the claim is removed.** No version from v1.2 onward contains a "0/10,000 under the gate" statement.

- The two runs with zero are `lumi-20261104-020310` (Qwen2.5-7B) and `lumi-20261110-031936` (Llama-3.3-70B); both contain 4,167 gated records, and their zero applies to the whole run, not to the gated subset.
- The two runs with one false success each are `lumi-20261110-002049` and `lumi-20261104-111050`; in both, that record lies outside the gated case types, so their gated subsets are also zero.
- The only gated denominator used in the paper is **30,798**, the sum over all 24 runs.

*Where:* §4.5 ("First, no aggregate in this paper is a '0/10,000 under the gate' claim"), Table 4.1, Appendix A.2.
*Recount:* `recount.py --lumi …` → `n=101140, guard=30798, fs_guard=0, fs=5696`.

## 2. "0/1,000 PASS risks cherry-picking; runs with 7 and 1 false successes exist alongside 0"

**Agreed.** All 24 runs are now listed with records and false successes (Appendix A.2), and §4.5 states that no run was selected because of its result. The text table (4.1) deliberately includes the 1,000-record runs with 7, 1 and 0 false successes.

*Where:* §4.5, Table 4.1, Appendix A.2.

## 3. "The 0.43% denominator: 53 false successes over 12,344 records, but all 53 lie among 918 probe records (≈5.8%)"

**Accepted; the ratio is not reported anywhere in v1.2.** The 12,344-record chained set is used only for integrity verification, and §3.1 now says explicitly that no rate in the paper is computed over it. The paper reports no percentage whose denominator is 12,344, and therefore no percentage that mixes probe and non-probe records.

*Where:* §3.1 (integrity paragraph), §6 item 5.

## 4. "36,550 is not one run; the text must carry the formula or the run ids"

**Withdrawn.** §4.5 states that the figure is not reproducible from the per-record `harness.guard` flags and is replaced by the countable 30,798 gated records. The same withdrawal was already in v1.1 and is retained.

*Where:* §4.5 (final paragraph), Appendix A.2 (the sum of all 24 runs is 101,140).

## 5. "Mistral runs show 99/200 false successes (~50%) but appear only as '400 records'; explain or separate them"

**Explained and separated.** The two Mistral runs are now in Table 4.1 and analysed in §4.5:

- 168 of their records are gated → **0** false successes; 232 are unguarded → **198** false successes.
- All 198 lie in the seven case types that were never gated.
- Their `false_note` values are `contains` (96), `exact` (68) and `refuse` (34) — answer-check categories, not tool-execution evidence categories. The pipeline compares the returned answer with the expected value; Mistral's answer did not satisfy the comparison.
- Conclusion stated in the paper: the 49.5% measures answer formatting and refusal under a fixed prompt set and is excluded from every cross-model statement.

*Recount:* `recount.py --lumi …` → `per_run['lumi-20261109-223741'] = {n: 200, guard: 84, fs: 99, fs_guard: 0}`, same for `…233200`.

## 6. "The controlled liar test is MockLiar, so 400/400 flagged is detection on a simulated liar"

**Accepted.** §4.6 now opens with "Condition B includes a simulated dishonest component (`MockLiar`)…", states that it does not adapt to the verifier and does not attempt evasion, and says explicitly that it must not be read as a sensitivity estimate for unconstrained agents. §6 item 1 retains the same point, and §5.4 already noted that latency comparisons include the mock component.

*Where:* §4.6, §6 item 1.

## 7. "Record is 'Software' v1.6.0, the preprint is v0.2.0, and Zenodo reports a newer version"

**Corrected.** The archive had v1.6.1 and v1.6.2 (both 19 November 2026) when this review was written.

- v1.2 cites the **concept DOI 10.5281/zenodo.23920505**, which always resolves to the latest version, and names v1.6.3 as the version that accompanies this revision (documentation-only change: corrected per-run README and a licence/provenance note). Previous versions are listed with their own DOIs: v1.6.2 = 10.5281/zenodo.24378026, v1.6.0 = 10.5281/zenodo.24369933.
- The data-file SHA-256 digests in §7 remain valid because v1.6.3 does not modify data files.
- The manuscript itself is deposited as a **new version of the preprint record** (v1.2), not as an attachment to a Software record; the artifact and the paper are separate objects with separate DOIs.

*Where:* §7, Appendix B, reference [2].

## 8. "Internal notes in the public dataset: `lumi/raw/README.md` contains a Bosnian TODO"

**Fixed in three places.** The file is rewritten in English as a data description, with no instructions to the authors:

- the Bosnian section "Mapiranje na brojeve iz teksta (paznja)" is replaced by "Mapping to numbers used in the manuscript", which lists the denominators actually used;
- the sentence "mora navesti tacne run_id-ove" is gone; the withdrawal of 36,550 is recorded as a fact about the archive;
- the run table now carries a `gated` column and a per-case table, so the file explains the structure instead of deferring to the paper.

The same content replaces the repository copy at `dataset/lumi/raw/README.md`, and the corrected file is deposited as `LUMI_RAW_README.md` in v1.6.3.

*Where:* repository `dataset/lumi/raw/README.md`, artifact `LUMI_RAW_README.md`.

## 9. "Raw records contain model text; check for sensitive data and for licence terms (Llama, Qwen, Mistral)"

**Checked, and documented.** A scan of all 101,140 `text` fields finds six e-mail-shaped strings, all placeholders (`vase_kompanije_email@domena.com`, `vaša.e.posta@kompanija.com`, `vaša.kompanija@domena.co`, `@adresa.com`), zero 13-digit identification numbers, and no telephone numbers (the single apparent match is a shell `PATH` string). Prompts are synthetic and derived from the authors' task templates; internal schema identifiers such as `vp2026` are retained because they are part of the prompt text.

Licences are now declared per model in §3.1 and in `LICENSES_AND_OUTPUTS.md`:

- Qwen2.5-7B and Mistral-Small-3.2-24B: Apache-2.0;
- Llama-3.3-70B: Llama 3.3 Community License, redistributed with attribution and without use of the outputs to train or improve another language model;
- a hash-and-length variant (no raw text for Llama runs) is derivable from the archive and reproduces every reported count, because all counts use `false_success`, `harness.guard`, `run_id` and `case` only.

*Where:* §3.1 (provenance and licences), §6 item 10, `LICENSES_AND_OUTPUTS.md`.

## 10. "The 50-task x 6-model audit and the 6,900-item corpus remain aggregates and must not be presented as reproducible"

**Agreed and already enforced.** Neither is in the quantitative findings; both are declared aggregate-only in §1.3 and in the note under Appendix A.3, with the reason (no per-record files in the archive). No claim in the paper depends on them.

*Where:* §1.3, Appendix A (closing note), §6 item 11.

---

## Two further corrections found while answering the above

### A. The gate is assigned by case type, and the paper now shows what that allows

`harness.guard` is a property of the case type within a run: `mp03`, `mp04`, `mp05`, `mp06` and `mp12` are gated; `mp01`, `mp02` and `mp07`–`mp11` never are. Of the 24 runs, 15 are fully gated in this sense, three 1,000-record runs armed the gate on a subset, and six runs (26,640 records) ran entirely without it.

That structure rules out a record-level randomised claim, but it does allow a case-level comparison, which v1.1 did not report. v1.2 adds it:

| Case type | Gate off: records | Gate off: FS | Gate on: records | Gate on: FS |
|---|---|---|---|---|
| `mp03` | 2,307 | 165 | 6,132 | 0 |
| `mp04` | 2,223 | 1,676 | 6,216 | 0 |
| `mp05` | 2,220 | 2,216 | 6,208 | 0 |
| `mp06` | 2,386 | 1,178 | 6,042 | 0 |
| `mp12` | 2,217 | 260 | 6,200 | 0 |
| **total, gated case types** | **11,353** | **5,495 (48.4%)** | **30,798** | **0** |
| never-gated case types | 58,989 | 201 (0.34%) | — | — |

The archive also contains a matched pair — two 10,000-record runs on the same model and day with identical `prompt_sha` for every case: `lumi-20261104-011605` (gate off) produced **1,683** false successes, `lumi-20261104-020310` (gate on) produced **0**.

The paper states what this does and does not support: case composition is controlled, run-level factors (time, order, unrecorded configuration) are not, no gated run was re-executed with the gate disarmed, and no effect size is estimated. A paired on/off run is named as the first item of planned work.

*Where:* §3.3.4, §4.5 (Tables 4.2 and 4.3), §5.5, §6 item 8, Appendix A.3.

### B. Provenance statement added

§3.1 now states the origin of the prompts, the absence of personal data, and the licence basis for the recorded outputs (see item 9). Appendix B carries the corresponding ethics statement.

---

## What changes for the reader in one paragraph

The record-level split (30,798 gated / 0; 70,342 unguarded / 5,696) stays, but it is no longer the evidence for anything: the paper now reports a case-matched comparison (5,495/11,353 against 0/30,798) and a same-day, same-model, same-prompt 10,000-record pair (1,683 against 0), states that both are quasi-experimental, withdraws the 0.43% and 36,550 figures, explains the Mistral runs as answer-check failures, labels the liar test as simulated, cites a version-resolved artifact, and publishes a dataset README with no internal notes.
