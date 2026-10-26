# Week Records

One file per week, `weeks/<ISO week>.md` (e.g. `2026-W44.md`), covering Monday to Sunday. The Check-in writes it for the coming week. The Review section is filled in at the following Check-in. Adjustments are appended as they happen. Terms follow `GLOSSARY.md`.

`weeks/` is ignored by the main repo and is its own git repo, so your log stays private. `examples/2026-W44.md` shows a completed Record.

## Format

```markdown
---
week: 2026-W44
start: 2026-10-26
level: normal
load_warning: none
ftp: 240
---

# 2026-W44 · Normal

## Plan

| Day | Date  | Session   | Workout            | Add-on     | Done  |
|-----|-------|-----------|--------------------|------------|-------|
| Mon | 10-26 | Recovery  | pt, str-a          |            |       |
| Tue | 10-27 | Quality   | th-2               |            |       |
| Wed | 10-28 | Endurance | end-ride-60        | addon-core |       |
| Thu | 10-29 | Quality   | ss-2               |            |       |
| Fri | 10-30 | Recovery  | pt                 |            |       |
| Sat | 10-31 | Endurance | end-ride-60-steps  |            |       |
| Sun | 11-01 | Endurance | end-ride-60-rolling|            |       |

## Reasoning

Why this Level, what life looks like this week, and any Load Warning and how it was answered.

## Adjustments

- 10-28: ran instead of riding (sunny) → run-easy-8-10

## Review

- Rides (intervals.icu): count, total time, anything notable
- Reported: runs, PT, walks you mentioned
- Ladders: th-2 at 6/10 → climb · ss-2 at 8/10 → repeat
- How the week felt

## Next

- Ladders: ss-2 · th-3 · vo2-2 · Tue → vo2max
- Strength → str-b · Add-on → addon-upper
- Last FTP test: 2026-10-20
```

## Fields

**Frontmatter**
- `week`, `start`: the ISO week and its Monday.
- `level`: `light` | `normal` | `push`.
- `load_warning`: `none`, or `"<rule>; accepted"`, or `"<rule>; overridden"`. The rule is one of `2 push weeks`, `3 normal+ weeks`, `form <= -20`, or `ramp > 6`. The Load Warning rules read this together with `level` from the last 3 Records.
- `ftp`: the FTP the week was planned against.

**Plan table.** The client script parses this table, so keep the columns in this order.
- `Session`: `Recovery` | `Quality` | `Endurance` | `Test`.
- `Workout`: one or more Bank IDs separated by commas, in the order done (`pt, str-a`). Leave it empty on a `Recovery` row for a full rest day, such as illness. In a partial week (a Week Record started mid-week), leave both `Session` and `Workout` empty on the unplanned days.
- `Add-on`: one Add-on ID or empty. Only allowed on Endurance and Test rows.
- `Done`, filled at the Review:
  - `✓` done
  - `✓ 6` a Quality Session done, with its effort (1–10)
  - `~` partly done
  - `✗` missed
  - `↔ run` an Endurance ride swapped for its run alternative

**Adjustments.** One dated line per change. The Plan table is edited to match, so it always shows the current plan, and this list keeps the history.

**Review.** Filled at the next Check-in:
- rides come from intervals.icu (completion and time);
- runs, PT and walks are what you report;
- the effort for each Quality Session is asked for then.

**Next.** The state carried into the following Check-in:
- the current step on each Ladder, after applying the climb rules in `bank/README.md`;
- which Ladder Tuesday uses next;
- the next Strength and Add-on in each cycle;
- the date of the last FTP test.

Before the first Record exists, start from the starting steps in `bank/README.md` (ss-2, th-2, vo2-2), Tuesday → threshold, str-a, addon-core, and last FTP test unknown (asked at the first Check-in).
