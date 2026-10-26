---
name: checkin
description: Weekly Check-in. Review the past week and plan the next Week Plan, then push it to intervals.icu. Use when the user wants to check in, plan next week, or do the Sunday planning.
---

# Check-in

Speak in the terms from `GLOSSARY.md`. The rules live in three places; read all three before step 1:

- `docs/planning-rules.md`: Week Templates, Load Warnings, Adjustment rules
- `bank/README.md`: picking and climbing rules, and the Workout index
- `docs/week-records.md`: the Week Record format

Ask the user's decisions with the AskUserQuestion tool, recommended option first.

The client is `scripts/icu.py`. Run it from the repo root.

## 1. Gather

1. **Target week:** the coming Mon–Sun. If today is Monday and the current week has no Week Record, plan the current week instead.
2. **Last week:** the most recent Week Record in `weeks/`. Also read the headers of the two before it.
3. **Ride data:** run `./scripts/icu.py rides <last Mon> <last Sun>` and `./scripts/icu.py fitness <today − 14> <today>`.
4. **No Week Record yet?** Use the starting state at the end of `docs/week-records.md`, ask for the date of the last FTP test, and skip step 2.

**Done when** you hold last week's Plan and Next block (or the starting state), the Levels of the last three weeks, last week's rides, and the latest fitness, fatigue, form and ramp numbers.

## 2. Review last week

1. Match the rides to the Plan rows.
2. Ask the user about the rest:
   - runs, PT and walks they did;
   - the effort (1–10) for each Quality Session;
   - anything that was missed or swapped;
   - how the week felt overall.
3. Fill in last week's record:
   - a `Done` value on every Plan row;
   - the Review section;
   - the Next block, applying the climbing rules from `bank/README.md` to each Quality Session's effort.

**Done when** every row of last week's Plan has a `Done` value, and the Next block states each Ladder's step, Tuesday's Ladder, the next Strength and Add-on, and the last FTP test date.

## 3. Shape the coming week

1. Ask about the week ahead: busy or fixed days, travel, energy and motivation.
2. Evaluate all four Load Warning rules. Report each as triggered, clear, or not enough data yet.
3. Ask the user to choose Light, Normal or Push. Recommend Light if any rule triggered. Otherwise recommend from their answers.

**Done when** the Level is chosen and every Load Warning rule has been reported.

## 4. Build the Week Plan

1. Fill the Week Template for the chosen Level with Workouts. Follow the picking rules in `bank/README.md`, starting from the Next block.
2. Fit the plan around the constraints from step 3, following the Adjustment rules.
3. Show it as the Plan table, adding each Workout's name and minutes for readability.
4. Iterate until the user approves.

**Done when** the user has approved a plan where every slot holds a Bank Workout that's allowed at this Level, and every picking rule holds:
- Ladder steps match the Next block;
- Tuesday is on the right Ladder;
- no Endurance Workout appears twice in the week;
- Strength and the Add-on are next in their cycles;
- the FTP test is placed if it's due.

## 5. Publish

1. Write `weeks/<week>.md`: frontmatter, the Plan table (Done column empty) and Reasoning, plus empty Adjustments and Review headings.
2. Run `./scripts/icu.py push-week weeks/<week>.md --dry-run`. Fix any plan problems it reports.
3. Run `./scripts/icu.py push-week weeks/<week>.md`.
4. Confirm with `./scripts/icu.py events <Mon> <next Mon>`. Report any push errors.
5. Commit both Week Records in the `weeks/` repo (`git -C weeks`) as "Check-in <week>: <Level>". If `weeks/` isn't a git repo yet, run `git init weeks` first.

**Done when** the events listing shows every planned Session plus the Check-in reminder, and the commit exists. Finish by telling the user their week in one line per day.
