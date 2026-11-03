# QUALIFICATION.md — dokazi izvršenih testova (2026-11-03)

> Napomena: „16 PASS“ u naslovu znači 16 testova; unutar tabele T6 je 16/16 podtestova — nisu isti broj.

Host: Contabo `vmi3557242` (Linux). Sve komande izvršene danas; PASS/FAIL iz stvarnog izlaza.

| # | Test | Komanda | Rezultat |
|---|---|---|---|
| T1 | Crossnode determinizam (normalizovano: bez `ms/probe_ms/task_ms/ts/executed_at/claimed_at`) | 2× `crossnode.py --demo`, SHA256 nad normalizovanim JSONL | **PASS** — oba `83f9c84a69b4ea4fb8be59797c2aae6e8b97b0ffbd2e64650ef62d7d24a3e4c5` |
| T2 | Crossnode demo (controlled) | `python3 crossnode.py --demo` | **PASS** — 48 records, 46 passed, 2 planted liars; **recall 2/2 (controlled), not a field rate** |
| T3 | EGR (hash-chain/Merkle) | `python3 tests/run_tests.py` | **PASS** — Ran 13, OK (2 skipped) |
| T4 | DSC determinizam | `python3 -m pytest -q` | **PASS** — **193 passed** (1,62 s) |
| T5 | GAMA lang | `python3 -m pytest -q` | **PASS** — **217 passed, 48 subtests** (35,5 s) |
| T6 | proofgate | `tests/run_tests.py` | **PASS** — 16/16 |
| T7 | polymorph | `tests/run_tests.py` | **PASS** — 15/15 |
| T8 | crossnode-bench tests | `tests/run_tests.py` | **PASS** — 10/10 |
| T9 | gamai_guard | `tests/run_tests.py` | **PASS** — 7/7 |
| T10 | agent-immunity | `tests/run_tests.py` | **PASS** — 40/40 |
| T11 | agent-immunity eval | `python3 eval.py` | **PASS** — ASR 1,0→0,0; false_denial 0,0; guard p50 **2.35 ms** (guard protocol, not probe latency) |
| T12 | srt sandbox | `tests/smoke.sh` | **PASS** — SANDBOX_OK / SMOKE_OK |
| T13 | GNP trust | `tests/smoke.sh` | **PASS** — SMOKE_OK |
| T14 | Harness health | `GET :7125/health` | **PASS** — 200, v9.4-fast-swarm |
| T15 | Harness MCP alati | `GET :7125/mcp/tools` | **PASS** — 468 (native 241 + Oracle 31 + 196) |
| T16 | Oracle MCP | `GET :8079/tools` | **PASS** — 31 |

## Napomene / ograničenja (pošteno)
- Crossnode demo je **sintetički** (node-a…e, 48 zapisa); javni artefakt 12.344 zapisa je odvojen i na mirroru.
- `agent-immunity` **guard p50 = 2,35 ms** je odvojen od crossnode task-latency (31,6 ms) — ne miješati u tekstu.
- Redroid kontejner **Exited (137)**, flota ga još prijavljuje online → popraviti ili ukloniti iz „online“.
- `gama-mcp` na Contabu **inactive**; ComfyUI :8188 **down**; kuća disk 0; gcp 958 MB — ograničenja flote.
- GitHub org 404 → javni dokaz ide kroz **mirror** (https://gamai.io/crossnode-bench/).
- LUMI: maintenance; v31 bez output artefakta; 25.600 planted trials još nije konsolidovan u javni evidence.
