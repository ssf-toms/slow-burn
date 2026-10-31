---
name: adjust
description: Mid-week Adjustment. Reshuffle the rest of the current Week Plan when life intervenes (sick, no time, travel, good weather), then re-push it to intervals.icu.
---

# Adjustment

Speak in the terms from `GLOSSARY.md`. Read `athlete/profile.md` first. If it's missing, stop and tell the user to run `/setup`.

The profile decides which rules apply (its Tiers, `places`, `pairings` and `alternatives`). Read these two files before step 1:

- `docs/planning-rules.md`: the Adjustment rules, including illness
- `bank/README.md`: picking rules and the Workout index

The Week Record format is in `docs/week-records.md`.

Ask the user's decisions with the AskUserQuestion tool, recommended option first.

The client is `scripts/icu.py`. Run it from the repo root.

## 1. Locate

1. **Week Record:** read the record in `athlete/weeks/` for the week containing today. If there isn't one, offer the Check-in instead and stop.
2. **What's done:** if ride is tiered, run `./scripts/icu.py rides <Mon> <today>` to see which rides are already done. Ask the user about the other Sessions so far.
3. **The change:** if the user's message leaves it unclear, ask what changed: which days, why, and whether it's known or still uncertain (for example, "might be sick tomorrow").

**Done when** you know which days are already done, which upcoming days are affected, and why.

## 2. Reshuffle

1. Rework only the days from the first affected day onward. Apply every Adjustment rule, and keep the Bank rules: Workouts allowed at this Level, Equipment at the day's Place (a moved Session keeps its ` @<place>`), pairings in `pairings`, and no Endurance Workout twice in the week.
   - **Strength:** a moved Strength Session or Add-on keeps its Exercises. If one is dropped, or the athlete wants different moves, recompose with picking rule 6 so the rest of the week's strength still covers squat, hinge, push, pull, carry and core where it can, and show the chosen Exercises by name.
2. Offer "swap to Alternative" for an Endurance Session only if `alternatives: on`. Otherwise Endurance Sessions move between days.
3. If a moved or swapped Session has no Workout the profile can fill, flag the gap and ask what to do instead (a Recovery row, or another real Bank Workout).
4. Show a before → after table of only the rows that change, with one line on each change's reason.
5. If a dropped Quality Session leaves the week lighter than its Level, say so plainly. The Week Level stays as recorded.
6. Iterate until the user approves.

**Done when** the user has approved, and the full remaining week passes every Adjustment rule:
- no back-to-back Quality Sessions;
- one Session a day;
- Add-ons only on Endurance and Test rows;
- every Workout's and Exercise's Equipment is at the day's Place, and every combined row is an allowed pairing;
- no Quality Session on the first day back from illness.

A same-day swap to the Alternative needs no reshuffle. Log it in Adjustments and skip to step 3's commit.

## 3. Publish

1. Edit the Plan table in place.
2. Append one dated line per change under Adjustments.
3. Run `./scripts/icu.py push-week athlete/weeks/<week>.md --from <first changed date> --dry-run`, then run it for real.
4. Confirm with `./scripts/icu.py events <first changed date> <Sun>`.
5. Commit in the `athlete/` repo (`git -C athlete`) as "Adjustment <week>: <short reason>".

**Done when** the events listing matches the remaining Plan rows and the commit exists. Finish by telling the user the rest of their week in one line per day.
