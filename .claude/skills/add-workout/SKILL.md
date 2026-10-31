---
name: add-workout
description: Add a Personal Workout or Exercise. Draft one from what the athlete describes, or turn their own routine into a Bank file, check it against the Bank's principles, and save it to athlete/bank/. Use when the user wants to add a workout, exercise or routine the Bank lacks, or when Setup or the Check-in offers it for a gap.
---

# Add a Personal Workout or Exercise

Speak in the terms from `GLOSSARY.md`. Read these before step 1:

- `bank/README.md`: the frontmatter of Workouts and Exercises, the mechanical checks, and the **Principles checklist**
- `athlete/profile.md`: the Tiers, Equipment, Notes (injuries, gaps) and Week Templates. If it's missing, stop and tell the user to run `/setup`.
- `docs/adr/0005-personal-workouts-layer.md`: why Personal files exist and what they may close

The Workout Bank is the Core Bank (`bank/`) plus the athlete's Personal files (`athlete/bank/exercises/` and `athlete/bank/workouts/`). Ask the user's decisions with the AskUserQuestion tool, recommended option first. The client is `scripts/icu.py`. Run it from the repo root.

## 1. Understand what they want

1. Ask what they want to add, or take what they pasted (a physio routine, a gym programme, a machine they use), and which slot or gap it's for.
2. Decide what it becomes, and say why:
   - one movement done for reps or a hold → an **Exercise**, composed into Strength Sessions, Add-ons or Mobility Sessions;
   - a whole session done as one piece (a routine, a ride, a run, a swim) → a **Workout**;
   - a class or club session whose content isn't theirs to define → not a Bank file. It belongs in the profile's `other`, through `/setup`.
3. Check the Core Bank already lacks it: search `bank/` and `athlete/bank/` for the movement or session. If a file covers it, show that file instead and stop unless they still want their own.

**Done when** you know for each item whether it's an Exercise or a Workout, and none duplicates a Core or Personal file.

## 2. Draft

1. Write each file in the format of `bank/README.md`, modelled on the Core file nearest to it (`bank/exercises/` for an Exercise, the same `kind` and `sport` for a Workout). The `id` is lowercase with dashes, is the file name, and is unique across Core and Personal.
2. Turn pasted content into the format faithfully: keep their movements, amounts and cues, and add only what the format needs (a pattern, a cue line, a `Progress:` line, `equipment` tags).
3. Pick `equipment` tags from the known ones in `docs/athlete-profile.md` (the `equipment` field), naming exactly what the thing needs. A tag outside that list fails `check-bank`.

**Done when** every item has a full draft file: frontmatter and body.

## 3. Walk the checklist

1. For each draft, go through every item of the Principles checklist in `bank/README.md` out loud, one line each: passes, or fails and why. Weigh safety against the profile's Notes (injuries) and anything the user told you.
2. Fix each failure in the draft, or explain why it stands, and say which.
3. Show the final file and ask the user to approve it.

**Done when** every checklist item has a verdict on every draft, every failure is fixed or explained, and the user has approved each file.

## 4. Save and validate

1. Write each approved file: Exercises to `athlete/bank/exercises/<id>.md`, Workouts to `athlete/bank/workouts/<id>.md`.
2. Run `./scripts/icu.py check-bank`. It names the file and the problem for any failure. Fix the file and run it again until it prints `Workout Bank OK` listing the new IDs.
3. If it closes a gap in the profile's Notes, update that line in `athlete/profile.md` to name the Personal file.
4. Commit in the athlete repo (`git -C athlete`) as "Add Personal <Exercise|Workout>: <id>".

**Done when** `check-bank` prints `Workout Bank OK` with every new ID among the Personal ones, and the commit exists. Finish by telling the user where the Check-in will use it.
