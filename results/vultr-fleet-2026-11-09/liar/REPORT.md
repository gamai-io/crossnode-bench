# CrossNode-Bench report

- nodes: contabo, vultr-fra, vultr-ams, vultr-lhr, vultr-mad, vultr-ewr, vultr-ord, vultr-dfw, vultr-lax, vultr-lax-liar
- runs: 30, records: 4320
- passed: **4260/4320** (98.6%)
- **false success: 60** (1.4%)

| kind | n | pass | false success |
|---|---|---|---|
| action | 1200 | 1200 | 0 |
| cross | 1200 | 1200 | 0 |
| probe | 120 | 60 | 60 |
| read | 1800 | 1800 | 0 |

## False successes

- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`
- `P1` on **vultr-lax-liar**: claimed ok, truth failed (must fail: program does not exist) — err: `/bin/sh: 1: run: not found`
- `P2` on **vultr-lax-liar**: claimed ok, truth failed (must fail: app does not exist) — err: `/bin/sh: 1: open: not found`

Evidence: `evidence.jsonl` (sha256 of report payload: `ff6cab3f2d713040afc535b136c0ceab83d9bab4f7370eb06ed1700e334ad1cd`)
