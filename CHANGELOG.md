# Changelog

All notable changes to this artifact. Format: Keep a Changelog, SemVer.

## [Unreleased]

### Added
- `pyproject.toml` (setuptools, `py-modules = ["crossnode"]`, `requires-python = ">=3.10"`,
  Apache-2.0, no runtime dependencies) so the benchmark can be installed with pip instead of
  copied: `pip install git+https://github.com/gamai-io/crossnode-bench@<sha>`. It adds the
  `crossnode` console script (same code path as `python3 crossnode.py`); no scoring, task or
  output changes.

## [1.7.0] - 2026-11-26

Scoring correctness release: tests for the scorer and three defects they exposed. No data files
and no published numbers change (`--demo` is still 48 records, 46 passed, 2 false successes).

### Added
- `tests/test_scoring.py` (pytest, stdlib-only code under test): claim-vs-truth for every task,
  pass/false-success definitions, probe honesty semantics, `MockLiar` scoping, exact aggregate
  arithmetic on synthetic record sets, node-level probe filtering, and a demo end-to-end check.
- `tests` job in `.github/workflows/ci.yml` (Python 3.10 and 3.12, < 30 s); the demo job now
  depends on it.

### Fixed
- `MockLiar` ignored `lies` and claimed success on any command containing its probe marker, so a
  liar configured for P1 could raise a false alarm on P2. `lies` is now authoritative and an
  empty map never lies.
- `judge()` derived the claim only from `result["ok"]`, so an adapter reporting just `rc` (allowed
  by the HTTP contract and by the README's "ok / rc") was scored as refusing every task. `ok`
  still wins when present; `rc == 0` is the fallback.
- A4's ground truth was unconditionally `True` even though its command ends in `test ! -e`;
  a failed assertion reported as success was scored as a pass. `truth_ok` is now `rc == 0`.

- `report.json` wrote an `evidence_sha256` computed over a re-serialised payload
  (`json.dumps(records, sort_keys=True)`) instead of the file, so nobody could check it with
  `sha256sum`. New runs store `evidence_file` plus the hash of the bytes on disk, and
  `python3 crossnode.py --verify-report <report.json>` recomputes the hash and every count.
  Reports published before this tag keep the old field; the README says not to trust it.

### Documentation
- README: explicit rate denominators (`passed / records`), the `ok`/`rc` claim rule, node-level
  probe filtering (not per probe id), and the A1/A2 structural-task caveat.

## [1.6.4] - 2026-11-24

Release for reproducibility requests: add the test set and the recorded configuration, change no data.

### Added
- `lumi_prompts_v1.json` — 12-case prompt set with expected answers; `sha256(prompt)` equals the
  `prompt_sha` field of the campaign records 12/12.
- `LUMI_RUN_MANIFEST.json` — per run: model and recorded model path, records, gated/ungated split,
  case types, repetitions per case, guard applied/version where documented, prompt-set hash,
  temperature 0 / seed 42, start/finish timestamps.
- `results.schema.json` v1.1 — optional `guard_version`, `guard_code_sha256`, `model_sha256`,
  `model_revision`, `tensor_parallel_size`, `max_num_seqs`, `temperature`, `seed`.

### Explicitly not available for the 2026-11 campaign
- model weight digests, tensor-parallel degree and `max_num_seqs` per run, per-record guard version
  (only the `harness.guard` boolean exists), guard code hash at run time.
  `LUMI_RUN_MANIFEST.json` lists these under `not_recorded`; the manifest states the guard version
  only for the five 2026-11-04 runs, where it is documented as v3.

### Unchanged
- All data files and their digests; every number in manuscript v1.2.

## [1.5.0] - 2026-11-10

LUMI MI250X campaign E1–E6 plus an objectively scorable benchmark suite (v2).

### Measured results
- **E1 (scale, FSR):** earlier "36,550 requests, 0 errors, 0 false successes" is **withdrawn** —
  not reproducible. v1.1 recount: **30,798 gated records, 0 false successes**; 70,342 unguarded records, 5,696 false successes (8.10%). LUMI 10k rerun: 1/10,000 (FAIL).
  Qwen2.5-7B: 88.2 rps @conc128 → **114.1 rps @conc256**; a 10,000-request run at
  conc512 gives **0/10,000** false success. Llama-3.3-70B: 22.6 → **28.7 rps**,
  0/5,000 per cell. Saturation points: 7B at conc256, 70B at conc256 (TTFT explodes
  at 512: 582 ms → 13.2 s).
- **E2 (reproducibility):** two identical runs at temperature 0 are **not
  bit-identical** under continuous batching: b1/b2/b5 match exactly, b4 differs in
  2/100 (79 vs 81). Claiming byte-identical generations would be false; the artifact
  reproduces deterministically only for generated data.
- **E3 (adaptive injection):** 203 attacks (paraphrase, Cyrillic homoglyphs, spaced
  letters, dots, zero-width, uppercase) + 200 benign controls incl. documentation
  questions. Existing keyword guard: **33.0% detection / 35.0% FP**. New intent guard
  (v2): **90.1% / 2.5%** in-sample, **85.7% / 3.5% out-of-sample** (seed 2028, never
  used for tuning). Target of 95% is **not** reached; keyword gating alone is
  insufficient, which is why action-level RiskGate remains mandatory.
- **E4 (ROCm portability):** TP1 61.7%, TP2 61.3%, TP4 60.6% on the same bench —
  within the E2 noise band; portability confirmed, quality difference not demonstrated.
- **E5 (scale, 70B):** 10,000 requests at conc512: `ok 10,000/10,000`,
  **false success 0/10,000**, verdict PASS.
- **E6 (deterministic invoice gate, BiH VAT 17%):** 500 invoices, 3 seeds:
  **recall 1,109/1,109 = 100%**, **FP 0/391**, Wilson 95% upper bound **0.97%** (≤1%).

### Added
- Benchmark v2: 700 generated, objectively scorable items in 4 blocks
  (`b1_arith` 300, `b2_needle` 100, `b4_honesty` 100, `b5_toolargs` 200), dataset
  SHA-256 `49c2f8ac4add1f6f7c5fae08692fef674b3c12433d7da45dfde4172044475157`.
- 9-model scoreboard (gpt-oss-120b 66.7%, Qwen2.5-7B 60.6%, Llama-3.3-70B 47.3%,
  Llama-Poro-70B 44.4%, Qwen2.5-VL-7B 48.4%).
- Deterministic-garbage detection: runs with >1% byte-level tokenizer artifacts are
  flagged `INVALID` instead of being reported as low scores (caught Mistral-3.1/3.2).
- `holdout_overlap.py`: leakage check of the private holdout against every dev set.
- `e7_reproduce.py`: independent reproduction of the deterministic artifacts.

### Fixed
- Guard bench: `max_tokens` was missing from the request payload, so vLLM generated
  up to `max_model_len` and 116/200 requests timed out. Now `--max-tokens 512`,
  `--timeout 300`, configurable `READY_TRIES` for 70B-class models.
- "Honest" checker counted the year in `DOC-2026` as a customer count; years and
  alphanumeric identifiers are now excluded (a 1/10,000 "false success" was a
  measurement false positive and is now 0/10,000).

### Known limitations
- Mistral-Small-3.1/3.2 are excluded: the HF tokenizer regex bug produces byte-level
  garbage; `--tokenizer-mode mistral` then trips the Pixtral multimodal processor.
- The 10k guard run reuses 12 prompt templates (~833 repetitions each); it is not
  10,000 distinct tasks.
- E3 guard v2 is tuned on seed 2027; out-of-sample numbers (seed 2028) are reported
  alongside.

## [1.4.0] - prior release
- Real 9-node Vultr fleet (200 rounds): 25,600 honest records, 0 false success;
  controlled liar run 400 false successes / 28,800, all 400 flagged.
