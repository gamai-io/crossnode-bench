# v1.4.0 — real multi-region Vultr fleet (200 rounds)

This release adds a real 9-node multi-region fleet run to the measurement pack.

## Included
- **Honest run:** Contabo + 8 Vultr `vc2-1c-1gb` (Ubuntu 24.04) in fra, ams, lhr, mad, ewr, ord, dfw, lax; 16 tasks × 200 rounds = **25,600 records**, 25,600/25,600 pass (100%), **0 false success**, p50 64.8 ms / p95 325.1 ms.
- **Controlled liar run:** same fleet plus one `MockLiar` wrapper around `vultr-lax`; **28,800 records**, 28,400/28,800 pass (98.61%), **400 false successes (1.39%)**, all 400 on the lying node (P1/P2), p50 171.3 ms / p95 332.7 ms.
- **Preprint v0.2.0** with §3.5 real-fleet section.
- **Dataset:** `dataset/vultr/aggregate.json`, `dataset/vultr/VULTR_2026-11-09.md`.

## Full results
- https://github.com/gamai-io/crossnode-bench/tree/main/results/vultr-fleet-2026-11-09-200
- `honest/evidence.jsonl.gz` sha256 `960b661424b2c2a147ad2179d15aeab357a34ce6e45b3e8564066fe824e87049`
- `liar/evidence.jsonl.gz` sha256 `372851594aae1ee554a46b817a0c466fad3edda4f3e9a0ecff2df9a081789674`

## Not included
- Raw Vultr per-trial logs in the Zenodo deposit (available in the GitHub results folder as gz).
- Vultr credentials/IPs (ephemeral).

## Caveats
- The liar is a controlled `MockLiar` wrapper, not a real compromised node; probes are synthetic and run only on nodes exposing a `probe` attribute.
- This is a detection test on real infrastructure, not a field false-success rate.
- Vultr IPs/instances are a 2026-11-09 snapshot; reproducibility is by protocol, not fixed hosts.
- No independent audit; preprint is not peer reviewed.

DOI: https://doi.org/10.5281/zenodo.24092188 (concept 10.5281/zenodo.23920505).

License: Apache-2.0.
