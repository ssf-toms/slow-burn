# Week Records

One file per week, `athlete/weeks/<ISO week>.md` (e.g. `2026-W44.md`), covering Monday to Sunday. The Check-in writes it for the coming week. The Review section is filled in at the following Check-in. Adjustments are appended as they happen. Terms follow `GLOSSARY.md`.

`athlete/` is ignored by the main repo and is its own git repo, so your Week Records stay private. It holds your Athlete Profile (`athlete/profile.md`, see `docs/athlete-profile.md`) and the Week Records in `athlete/weeks/`. `examples/2026-W44.md` shows a completed Record.

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

| Day | Date  | Session   | Workout                                                        | Add-on                 | Done  |
|-----|-------|-----------|----------------------------------------------------------------|------------------------|-------|
| Mon | 10-26 | Strength  | pt, kb-goblet-squat, kb-swing, push-up, band-row, dead-bug     |                        |       |
| Tue | 10-27 | Quality   | th-2                                                           |                        |       |
| Wed | 10-28 | Endurance | end-ride-60                                                    | kb-suitcase-carry, bird-dog |  |
| Thu | 10-29 | Quality   | ss-2                                                           |                        |       |
| Fri | 10-30 | Recovery  | pt                                                             |                        |       |
| Sat | 10-31 | Endurance | end-ride-60-steps                                              |                        |       |
| Sun | 11-01 | Endurance | end-ride-60-rolling                                            |                        |       |

## Reasoning

Why this Level, what life looks like this week, any Load Warning and how it was answered, and any change to the Athlete Profile since last week.

## Adjustments

- 10-28: ran instead of riding (sunny) → run-easy-8-10

## Review

- Rides (intervals.icu): count, total time, anything notable
- Reported: runs, swims, PT, walks you mentioned
- Ladders: th-2 at 6/10 → climb · ss-2 at 8/10 → repeat
- How the week felt

## Next

- Ladders: ride: ss-2 · th-3 · vo2-2 · Tue → vo2max
- Last FTP test: 2026-10-20
```

## Fields

**Frontmatter**
- `week`, `start`: the ISO week and its Monday.
- `level`: `light` | `normal` | `push`.
- `load_warning`: `none`, or `"<rule>; accepted"`, or `"<rule>; overridden"`. The rule is one of `2 push weeks`, `3 normal+ weeks`, `form <= -20`, or `ramp > 6`. The Load Warning rules read this together with `level` from the last 3 Records.
- `ftp`: the FTP the week was planned against.

**Plan table.** The client script parses this table, so keep the columns in this order.
- `Session`: `Recovery` | `Quality` | `Endurance` | `Strength` | `Other` | `Test`. `Strength` and `Other` come from the Week Template's cells of those kinds (`docs/athlete-profile.md`).
- `Workout`: one or more Bank IDs separated by commas, in the order done (`pt, kb-goblet-squat, kb-swing, push-up, band-row, dead-bug`). Consecutive Exercise IDs form one composed block, pushed as one note "Strength (N rounds)" with the rounds from `level` (picking rule 6 in `bank/README.md`). So a Workout and a composed block can be paired (`pt, …` above is a PT + strength pairing). In a Push week, one Quality ride may carry an Extension, `+<minutes>` after its ID (`th-2 +15`): 10–15 extra minutes at Endurance before the cooldown (picking rule 4 in `bank/README.md`). Leave it empty on a `Recovery` row for a full rest day, such as illness. In a partial week (a Week Record started mid-week), leave both `Session` and `Workout` empty on the unplanned days.
- `Add-on`: empty, or the IDs of 2–4 Exercises separated by commas (`kb-suitcase-carry, bird-dog`), pushed as one note "Add-on (N rounds)". Only allowed on Endurance and Test rows.
- `Done`, filled at the Review:
  - `✓` done
  - `✓ 6` a Quality Session done, with its effort (1–10)
  - `~` partly done
  - `✗` missed
  - `↔ run` an Endurance Session swapped for its Alternative, naming the sport (`↔ run`, `↔ swim`, `↔ ride`)

**Adjustments.** One dated line per change. The Plan table is edited to match, so it always shows the current plan, and this list records every change.

**Review.** Filled at the next Check-in:
- rides come from intervals.icu (completion and time);
- runs, swims, PT and walks are what you report;
- the effort for each Quality Session is asked for then.

**Next.** The state carried into the following Check-in:
- the current step on each Ladder, grouped by sport (`ride: ss-2 · th-3 · vo2-2`), after applying the climb rules in `bank/README.md`;
- which Ladder the rotating Quality slot uses next (the first Quality day for the maintainer: `Tue → vo2max`);
- the date of the last FTP test, when ride is Primary, and of the last run test, when run is Primary.

**Profile changes.** When the Athlete Profile changes (new Equipment, a Sport Tier moved, regenerated Week Templates), say so in that week's Reasoning, so the Records explain why the plan's shape changed.

**Older Records.** Records written before the Athlete Profile existed stay as they are. So do Records naming the retired strength IDs (`str-a`, `addon-core`, …): they're history, not pushed again, and `bank/README.md` maps each to its Exercises. A Monday row such as `Recovery | pt, str-a` stays as written, and the Load Warning rules only read `level`.

Before the first Record exists, start from the starting steps in `bank/README.md` (set by `experience` in the Athlete Profile; `some` gives ss-2, th-2, vo2-2), the rotating Quality slot on its first Ladder (threshold for the maintainer), and last FTP test unknown (asked at the first Check-in).
