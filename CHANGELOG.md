# Changelog

All notable changes to this artifact. Format: Keep a Changelog, SemVer.

## [1.5.0] - 2026-11-10

LUMI MI250X campaign E1–E6 plus an objectively scorable benchmark suite (v2).

### Measured results
- **E1 (scale, FSR):** 10 cells, **36,550 requests, 0 errors, 0 false successes**.
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
