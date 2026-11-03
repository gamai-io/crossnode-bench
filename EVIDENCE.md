# Evidence pack

Turns the public JSONL into a tamper-evident artifact: a per-record SHA-256 chain plus a
Merkle root over the record hashes. The rules are fixed here so a third party can
recompute them without our code.

## Rules (normative)

- Canonicalization: JSON with sorted keys, compact separators (`,` `:`), UTF-8.
- One record: `body = record without "hash", plus "prev_hash"`; `hash = sha256(canon(body))`.
- The first record uses `prev_hash = "0" * 64`.
- Merkle: pairwise `sha256((h1 + h2).encode())` over lowercase hex strings; if a level has
  an odd number of hashes, the last one is duplicated.
- The manifest contains no timestamps, so the same input yields byte-identical output.

## Commands

```bash
python3 tools/evidence.py chain \
  --in evidence_all.jsonl \
  --out evidence_chained.jsonl \
  --manifest manifest.json \
  --expect-records 12344

python3 tools/evidence.py verify \
  --in evidence_chained.jsonl \
  --manifest manifest.json
```

Current public artifact (2026-11-03, 12,344 records):

- `source_sha256: 2a3ca84f8f8d18f2e8aae57cc37da7cb211f7711d731172f58f629d562ff3282`
- `merkle_root:    eda02d9cd4ff14d594d144c2d319bb3a3d1ea16569638238be14779da3d11d2d`
- Determinism: two independent runs produced identical file and manifest SHA-256
  (`e79a43f4…` and `a84642af…`).

## Gate

`gate.rego` denies when the artifact is unsigned, has no records, exceeds the
false-success threshold (default 0.02), or falls below the coverage threshold (default
0.95). `gate.sh` is the local fallback: it verifies the chain, then uses `opa` if
installed, otherwise a built-in check with the same thresholds.

```bash
./gate.sh evidence_chained.jsonl manifest.json true 0.02 0.95   # allow
./gate.sh evidence_chained.jsonl manifest.json false 0.02 0.95  # deny (unsigned)
```

## CI

`.github/workflows/evidence.yml` (GitHub-hosted runner):

1. fetch the public artifact from the static mirror;
2. build and verify the chain;
3. keyless `cosign sign-blob` (GitHub OIDC);
4. build an in-toto statement and `cosign attest-blob` it;
5. run the OPA gate; unsigned evidence must be rejected;
6. upload the chained artifact, manifest, bundle and attestation.

## What is built / what is not

Built: chain + Merkle + manifest generator, verifier, JSON schemas, Rego policy, local
gate, CI workflow, deterministic output.

Not built: DOI (Zenodo), hardware root of trust / TPM attestation, live OTel exporter
(only the attribute contract), KMS-backed signing (keyless OIDC needs GitHub), and a
public leaderboard. Do not claim those exist.

## Acceptance tests (third party)

1. `python3 tools/evidence.py verify ...` → `{"ok":true,...}` on the published artifact.
2. Flip one byte in a record → `verify` exits 1 with `FAIL hash at line N`.
3. Replace `merkle_root` in the manifest → verify exits 1.
4. `./gate.sh ... false` → exits 1 (`evidence is not signed`).
5. `./gate.sh ... true` with thresholds 0.02/0.95 → exits 0.
