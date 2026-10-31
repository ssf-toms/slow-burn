---
name: checkin
description: Weekly Check-in. Review the past week and plan the next Week Plan, then push it to intervals.icu. Use when the user wants to check in, plan next week, or do the Sunday planning.
---

# Check-in

Speak in the terms from `GLOSSARY.md`. Read `athlete/profile.md` first. If it's missing, stop and tell the user to run `/setup`.

The profile decides which rules apply. "Ride is tiered" means `tiers` lists `ride`; "ride is Primary" means it's `primary`. The rules live in four places; read all four before step 1:

- `docs/athlete-profile.md`: the profile fields and the template cell syntax
- `docs/planning-rules.md`: Load Warnings, Adjustment rules, and the conditional parts (generation rule 7)
- `bank/README.md`: picking and climbing rules, and the Workout index. The Workout Bank also holds the athlete's Personal Workouts and Exercises in `athlete/bank/`: list them with `ls -R athlete/bank` and read their frontmatter
- `docs/week-records.md`: the Week Record format

Ask the user's decisions with the AskUserQuestion tool, recommended option first.

The client is `scripts/icu.py`. Run it from the repo root.

## 1. Gather

1. **Profile:** hold the fields and the `## Week Templates` table from `athlete/profile.md`, plus the gaps in its Notes.
2. **Target week:** the coming Mon–Sun. If today is Monday and the current week has no Week Record, plan the current week instead.
3. **Last week:** the most recent Week Record in `athlete/weeks/`. Also read the headers of the two before it.
4. **Ride data**, only if ride is tiered: run `./scripts/icu.py rides <last Mon> <last Sun>` and `./scripts/icu.py fitness <today − 14> <today>`.
5. **No Week Record yet?** Use the starting state at the end of `docs/week-records.md`. If ride is Primary, ask for the date of the last FTP test, and if run is Primary, of the last run test. Skip step 2.

**Done when** you hold the profile and its templates, last week's Plan and Next block (or the starting state), and the Levels of the last three weeks; plus, if ride is tiered, last week's rides and the latest fitness, fatigue, form and ramp numbers.

## 2. Review last week

1. Match the rides (if any) to the Plan rows.
2. Ask the user about the rest:
   - the Sessions not in the ride data: runs, swims, strength, mobility, walks, `other` activities;
   - the effort (1–10) for each Quality Session;
   - anything that was missed or swapped;
   - how the week felt overall.
3. Fill in last week's record:
   - a `Done` value on every Plan row;
   - the Review section;
   - the Next block, applying the climbing rules from `bank/README.md` to each Quality Session's effort.

**Done when** every row of last week's Plan has a `Done` value, and the Next block holds every line `docs/week-records.md` requires for this profile: each Ladder's step and the rotating slot's next Ladder (if any Primary sport has Ladders), and the last FTP test date (if ride is Primary).

## 3. Shape the coming week

1. Ask about the week ahead: busy or fixed days, travel, energy and motivation.
2. Evaluate the Load Warning rules. Rules 1 and 2 always apply. Rules 3 and 4 apply only if ride is Primary or Secondary (not Occasional); otherwise report them as "n/a: ride not Primary or Secondary" and weigh the reported Sessions by judgement.
3. Ask the user to choose Light, Normal or Push. Recommend Light if any rule triggered. Otherwise recommend from their answers.

**Done when** the Level is chosen and every Load Warning rule has been reported as triggered, clear, not enough data yet, or n/a: ride not Primary or Secondary.

## 4. Build the Week Plan

1. Take the profile's Week Template column for the chosen Level. The template is the athlete's approved shape: fill it, never regenerate it or use the worked example in `docs/planning-rules.md`.
2. Fill each cell with Bank Workouts the profile allows, following the picking rules in `bank/README.md` from the Next block. Pick each Dose by Level. In every cell, resolve each ` or ` choice, and name the Alternative on Endurance Sessions only if `alternatives: on`.
   - **Strength** (if tiered): compose each Strength Session and Add-on from Exercises with picking rule 6: aim for 5–6 Exercises a Session and 2–3 an Add-on (`push-week` only rejects clear mistakes, outside 3–8 and 2–4), the week's strength together covering squat, hinge, push, pull, carry and core (a lone Session is full-body), preferring Exercises not in last week's Plan. Write the Exercise IDs in the cell, in order; rounds come from the Level.
   - **Mobility** (if tiered): fill each Mobility Session with picking rule 9: a whole `kind: mobility` Workout, 6–8 mobility Exercises, or a Workout plus 2–3 Exercises. Vary the mix across the week, following any preference in the profile's Notes, and prefer mobility Exercises not in last week's Plan.
3. **Gaps:** a slot a Personal Workout or Exercise fills is not a gap, even if the profile's Notes still list it: say so, so Setup's Notes can drop it. A cell the Workout Bank, Core and Personal, can't fill (a sport with no Workouts, missing Equipment, no FTP test without a smart trainer) stays in the plan as a flagged row. Ask the user what to do instead ("swim slot: no pool in the profile → walk or rest?"), and fill it only with a Bank Workout, a Recovery row, or a new Personal file added through `/add-workout` first.
4. Fit the plan around the constraints from step 3, following the Adjustment rules.
5. Show it as the Plan table, adding each Workout's name and minutes for readability, with each gap marked. For each Strength Session, Add-on and composed Mobility Session, list the chosen Exercises by name with their reps or hold and pattern, and the rounds, so the athlete can swap any they dislike.
6. Iterate until the user approves.

**Done when** the user has approved a plan where every slot holds a Bank Workout or `other:<id>` from the profile, allowed at this Level, or is a gap the user has decided on; and every rule holds:
- **Equipment:** every Workout's and Exercise's `equipment` tags are at the day's Place (its ` @<place>`, copied from the template cell into the Session cell, or the default Place);
- **Pairings:** a row combines Workouts only if the pair is in `pairings`, and nothing is paired with a Quality Session;
- **Ladders** (if any Primary sport has Ladders): steps match the Next block, and each Quality slot is on the Ladder the pairing rule gives it;
- no Endurance Workout appears twice in the week;
- ride lengths are within the Level's range, and an Extension, if any, is on one Quality ride in a Push week (picking rule 4);
- strength follows picking rule 6 (if tiered): sizes, all six patterns across the week (across two or three weeks when the week's only strength is Add-ons), no Exercise twice in a row, and mostly different Exercises from last week;
- the FTP test (`ftp-ramp-test`, or the athlete's Personal ride test) is placed if it's due (if ride is Primary), and the run test if it's due (if run is Primary).

## 5. Publish

1. Write `athlete/weeks/<week>.md`: frontmatter, the Plan table (Done column empty) and Reasoning, plus empty Adjustments and Review headings.
   - Write `ftp` from the profile if ride is tiered; leave it out otherwise.
   - In Reasoning, name each gap and what the user chose instead.
   - Run `git -C athlete log --oneline -10`. If a commit touching `profile.md` (a "Setup: …" commit) is newer than the last "Check-in" commit, say in Reasoning what changed in the profile.
2. Run `./scripts/icu.py push-week athlete/weeks/<week>.md --dry-run`. Fix any plan problems it reports.
3. Run `./scripts/icu.py push-week athlete/weeks/<week>.md`.
4. Confirm with `./scripts/icu.py events <Mon> <next Mon>`. Report any push errors.
5. Commit both Week Records in the `athlete/` repo (`git -C athlete`) as "Check-in <week>: <Level>".

**Done when** the events listing shows every planned Session plus the Check-in reminder, and the commit exists. Finish by telling the user their week in one line per day, gaps included.
