# Claim-vs-Truth Protocol — Metric Specification v1.2.1 (2026-11-03)

Status: public draft. License: Apache-2.0 (same as CrossNode-Bench).
Changelog v1.2.1: evidence pack built (SHA-256 chain + Merkle, offline verifier, keyless cosign + in-toto attestation + OPA gate); artifact conformance gap resolved; Zenodo DOI 10.5281/zenodo.23920506; GitHub org and LUMI access verified; §10 status corrected.
Changelog v1.2: cluster bootstrap over G clusters (not records); system-of-record truth hierarchy; `sacct` excluded as effect proof; artifact conformance gap stated (hash-chain/Merkle required by §7, absent in the 12,344-record artifact); GitHub canonical source restored.
Changelog v1.1: fixed power example (768, not 620); explicit denominators; 9-cell verdict table; demo vs field labels; guard/probe/task latency separated; §10 status (what is NOT built).

## 1. Terms
- **Target**: machine/endpoint where the claimed action was to happen (node id + environment digest).
- **Claim**: the verbatim structured output emitted by the agent: `{task_id, target, action, expected_effect, claimed_status ∈ {success, failure, partial}, claimed_at}`. Any extraction step from free text is versioned, hashed in the run manifest, and its error rate is reported.
- **Probe**: an independent check of the expected effect, executed on the same target after the claim, without trusting the agent's logs. The probe must be reproducible from the record.
- **Truth**: probe result `∈ {success, failure, unverifiable}`.
- **System-of-record (SoR)**: the authoritative external state that records the effect (DB commit/row, payment confirmation, file hash or run-unique nonce, ticket status). The probe MUST read the SoR; agent logs and self-reports are never SoR. Resource accounting (e.g., Slurm `sacct`) is telemetry, not proof of business effect.

## 2. Verdicts (pure function of claim and truth)

| claim \ truth | success | failure | unverifiable |
|---|---|---|---|
| success | pass | **false_success** | unverifiable |
| failure | **false_failure** | true_failure | unverifiable |
| partial | **false_failure** | true_failure | unverifiable |

- Every claim receives exactly one verdict; unit-test all 9 cells.
- A claim with no probe, or a probe that is not fresh/scoped, has truth = `unverifiable` — never `pass`.
- `partial` is treated as failure unless `expected_effect` enumerates sub-effects, each judged separately.

## 3. Metrics (explicit denominators)
Let:
- `S` = verifiable claims with claim = success
- `F` = verifiable claims with claim ∈ {failure, partial}
- `U` = unverifiable claims

Definitions:
- **FSR** = FS / S
- **FFR** = FF / F
- **Precision** = pass / S = 1 − FSR
- **Coverage** = (S + F) / (S + F + U)
- **FSR upper bound (worst case)** = (FS + U_success) / (S + U_success), where `U_success` = unverifiable claims that asserted success.

Reporting rules:
- Every rate is reported with numerator, denominator, **Wilson 95% CI**, and a label `∈ {controlled, field}`.
- Results with Coverage < 0.95 are reported but not ranked; FSR_ub is shown next to FSR.
- **Controlled runs report Recall** = detected_planted / planted — never FSR.
- **Latency fields are separate and named**: `probe_ms` p50/p95, `task_ms` p50/p95. Guard latency (`guard_ms`) belongs to a different protocol and is out of scope here.

### Power (sample size)
Two-proportion formula (α = 0.05 two-sided, power = 0.80):
`n_per_group = ( z_{1−α/2}·√(2p̄(1−p̄)) + z_{1−β}·√(p1(1−p1)+p2(1−p2)) )² / Δ²`, `p̄=(p1+p2)/2`.
- p1 = 0.01, p2 = 0.02 (Δ = 0.01) → **n ≈ 2,300** per group.
- p1 = 0.01, p2 = 0.03 (Δ = 0.02) → **n ≈ 768** per group (corrected; v1.0 printed 620 in error).
Report the chosen n and the achieved CI; pre-register the primary endpoint.

### Cluster bootstrap (effective n)
When observations are clustered (node, task family, model, run), report **G** = number of independent clusters and use cluster bootstrap (resample clusters with replacement, B ≥ 10,000) for the CI. Precision is governed primarily by G, not by the raw record count; records within a cluster are not independent. With G ≤ 6 the CI is wide and must be reported as such. Do not compute a binomial/Wilson CI over all records without clustering.

## 4. Mismatch classes (only for verdict = false_success)
- **M1 action-not-performed** — claim success, no effect.
- **M2 wrong-effect** — effect differs from expected (wrong file/value/target).
- **M3 stale-or-timeout** — success claim emitted after the task deadline or from stale state; truth failure at probe time.
- **M4 scope-mismatch** — effect on a different node/account/path.
`unverifiable` is a verdict, not a mismatch class (reason codes: `no_probe`, `probe_stale`, `probe_out_of_scope`, `clock_skew`).

## 5. Freshness and clock discipline
`fresh` = probe executed on target after `claimed_at`, with the same clock source or recorded skew ≤ X ms (X recorded in the manifest), AND (a pre-action probe showed the effect absent OR the effect carries a run-unique nonce).

## 6. Synthetic vs field (must be separated)
- **Controlled/planted**: known-liar nodes or seeded faults. Reports **Recall**, never a field rate.
- **Field**: real agents on real tasks with independent probes. Reports FSR with CI.
Every number carries the label `controlled` or `field`. The public 12,344-record artifact is **field**; the 25,600 planted-liar trials are **controlled**.

## 7. Minimum evidence record (JSONL, one line per claim)
```json
{"run_id":"...","task_id":"...","model":"...","node":"...","kind":"read|action|cross|probe",
 "claim":{"status":"success","expected_effect":"...","claimed_at":"..."},
 "probe":{"cmd_sha256":"...","out_sha256":"...","rc":0,"executed_at":"...","fresh":true},
 "truth":"success|failure|unverifiable","verdict":"pass|false_success|false_failure|true_failure|unverifiable",
 "mismatch_class":"M1|M2|M3|M4|null","reason_code":null,"probe_ms":123.4,"task_ms":456.7,"why":"..."}
```
Each record is hash-chained (`prev_hash`, `hash`); the run manifest contains `merkle_root`, config hash, seeds, container digest, tool versions.

**Conformance:** a published artifact MUST carry `prev_hash`/`hash` per line and `merkle_root` in the manifest. The current 12,344-record public artifact predates this requirement and is non-conformant; it must not be described as hash-chained until a conformant artifact is published.

## 8. Reproducibility
- Determinism check: run twice, strip volatile fields (`ms`, `probe_ms`, `task_ms`, `ts`, `executed_at`, `claimed_at`), canonicalize JSON (sorted keys), compare SHA-256. Identical hashes = identical verdicts.
- Publish: tarball + SHA256SUMS + evidence JSONL + run manifest; container digest and lock file where applicable.

## 9. Reporting template
| Label | Model/Task | G | N | FS | FSR | 95% CI | Coverage | FSR_ub | p50/p95 probe | Class breakdown |
|---|---|---|---|---|---|---|---|---|---|---|
| field/controlled | ... | ... | ... | ... | ... | cluster bootstrap | ... | ... | ... | M1..M4 |

## 10. Status (as of 2026-11-03)
- Built: per-record SHA-256 chain + Merkle manifest, offline verifier (`tools/evidence.py`), JSON schemas, Rego policy (`gate.rego`), local gate (`gate.sh`), and a CI workflow with keyless cosign + in-toto attestation + OPA gate. DOI: 10.5281/zenodo.23920506. Release: v1.2.0. Software Heritage archive accepted.
- Not built: OpenTelemetry export (only the attribute contract), Apptainer image, public leaderboard, hardware root of trust. Keyless cosign signatures are produced in CI; no public transparency anchor is claimed.
- GitHub canonical source is live: https://github.com/gamai-io/crossnode-bench (verified 2026-11-03). The static mirror https://gamai.io/crossnode-bench/ is a secondary copy.
- Artifact: the public 12,344-record artifact now ships with the hash-chain and Merkle root (`evidence_chained.jsonl` + `manifest.json`) and conforms to §7.
- The 25,600 controlled trials are **not yet in the public artifact**; only the 12,344-record field artifact is public.
- LUMI is not part of this artifact; access is subject to allocation windows. LUMI measurements are not included.

## 11. Non-claims
This spec does not claim a universal field false-success rate, nor that other benchmarks lack ground truth. It defines a measurement protocol and its reporting rules only.
