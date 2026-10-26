---
name: adjust
description: Mid-week Adjustment. Reshuffle the rest of the current Week Plan when life intervenes (sick, no time, travel, good weather), then re-push it to intervals.icu.
---

# Adjustment

Speak in the terms from `GLOSSARY.md`. Read these two files before step 1:

- `docs/planning-rules.md`: the Adjustment rules, including illness
- `bank/README.md`: picking rules and the Workout index

The Week Record format is in `docs/week-records.md`.

Ask the user's decisions with the AskUserQuestion tool, recommended option first.

The client is `scripts/icu.py`. Run it from the repo root.

## 1. Locate

1. **Week Record:** read the record for the week containing today. If there isn't one, offer the Check-in instead and stop.
2. **What's done:** run `./scripts/icu.py rides <Mon> <today>` to see which rides are already done.
3. **The change:** if the user's message leaves it unclear, ask what changed: which days, why, and whether it's known or still uncertain (for example, "might be sick tomorrow").

**Done when** you know which days are already done, which upcoming days are affected, and why.

## 2. Reshuffle

1. Rework only the days from the first affected day onward. Apply every Adjustment rule, and keep the Bank rules: Workouts allowed at this Level, and no Endurance Workout twice in the week.
2. Show a before → after table of only the rows that change, with one line on each change's reason.
3. If a dropped Quality Session leaves the week lighter than its Level, say so plainly. The Week Level stays as recorded.
4. Iterate until the user approves.

**Done when** the user has approved, and the full remaining week passes every Adjustment rule:
- no back-to-back Quality Sessions;
- one Session a day;
- Add-ons only on Endurance and Test rows;
- no Quality Session on the first day back from illness.

A same-day ride → run swap needs no reshuffle. Log it in Adjustments and skip to step 3's commit.

## 3. Publish

1. Edit the Plan table in place.
2. Append one dated line per change under Adjustments.
3. Run `./scripts/icu.py push-week weeks/<week>.md --from <first changed date> --dry-run`, then run it for real.
4. Confirm with `./scripts/icu.py events <first changed date> <Sun>`.
5. Commit in the `weeks/` repo (`git -C weeks`) as "Adjustment <week>: <short reason>".

**Done when** the events listing matches the remaining Plan rows and the commit exists. Finish by telling the user the rest of their week in one line per day.
