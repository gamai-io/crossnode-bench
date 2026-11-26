# v1.7.0 — the scorer is tested, and reports are verifiable

No data file changed. `python3 crossnode.py --demo` is still **48 records, 46 passed,
2 false successes**, and every figure in the published v1.4.0/v1.5.x results stands.

## Why this release exists

The benchmark's product is a number that somebody else can check. That number was produced
by a scorer with no tests. `tests/test_scoring.py` (101 cases) now pins the scoring path and
exposed three defects:

| # | Defect | Effect |
|---|---|---|
| 1 | `MockLiar` lied on any command containing its probe marker, ignoring `lies` | a liar configured for P1 could raise a false alarm on P2 — a *wrong* detection attributed to the detector |
| 2 | `judge()` read only `result["ok"]` | an adapter replying `{"rc": 0}` (allowed by the HTTP contract) was scored as failing every task |
| 3 | A4's ground truth was unconditionally `True` | a node whose in-command `test ! -e` returned 1 was recorded as a pass; the false success was lost |

Fixes are covered by tests; reverting them fails 5 of 101.

## Reports are now checkable

`report.json` used to carry `evidence_sha256` over a re-serialised payload, not over the file —
unverifiable by construction. New runs write `evidence_file` and the sha256 of the bytes on
disk. `--verify-report` recomputes the hash and every count from the records:

```
$ python3 crossnode.py --verify-report runs/<stamp>/report.json
{"ok": true, "problems": [], "sha256": "4f8e640c…", "counts": {"records": 48, "passed": 46, "false_success": 2}}
```

**Action for anyone holding an older report:** the counts are still valid (recompute them from
the records), but the `evidence_sha256` field in reports published before 2026-11-26 does not
match the file and must not be used as a trust anchor.

## What this does not change

- No result file, no prompt set, no manifest, no published pass rate.
- Probe filtering is node-level (an adapter opt-in), as before; the README now says so instead
  of implying per-probe-id filtering.
