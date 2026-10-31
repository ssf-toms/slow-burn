# Workout Bank

The curated set of Workouts and Exercises every Week Plan draws from (see `GLOSSARY.md`), plus the athlete's Personal ones (below). There's one file per Workout, and one per Exercise in `exercises/`. The frontmatter holds the fields the Check-in uses to pick Workouts. Ride bodies hold an `intervals` block (intervals.icu workout text) that is pushed to intervals.icu and synced to MyWhoosh.

Ride targets are **%FTP** with simple steps and repeats, and no ramps or cadence targets (ADR 0001). Example watts at FTP 240:

| Zone | %FTP | Watts |
|------|------|-------|
| Endurance (Zone 2) | 62–74% | 150–178 W |
| Sweet Spot | 88–92% | 211–221 W |
| Threshold | 95–97% | 228–233 W |
| VO2max | 110–112% | 264–269 W |

## Frontmatter

| Field | Value | Meaning |
|-------|-------|---------|
| `id` | lowercase, dashes | The name used in Week Records. Same as the file name. |
| `name` | string | The calendar title. |
| `kind` | `quality` \| `endurance` \| `mobility` \| `recovery` \| `test` | What the Workout is for. |
| `sport` | `ride` \| `run` \| `swim` \| `walk` \| `strength` \| `mobility` | The activity. |
| `duration_min` | number | Typical length in minutes. |
| `equipment` | list of tags, `[]` for none | The Equipment the Workout needs, from the tags in `docs/athlete-profile.md` (`bodyweight`, `bands`, `band-anchor`, `kettlebell`, `dumbbells`, `barbell`, `bench`, `cable`, `pull-up-bar`, `machines`, `smart-trainer`, `pool`, `hr-strap`). It can only be planned on a day whose Place has every tag. The one exception: `smart-trainer` on a `delivery: workout` ride only decides whether it's pushed as indoor or outdoor, so the ride can be planned without one. Required in every file. |
| `delivery` | `workout` \| `note` | `workout` is pushed as a structured workout (rides). `note` is a calendar note. |
| `ladder`, `step` | Ladder name, number | Quality Workouts only: which Ladder, and which step on it. |
| `variant_group` | string | Workouts that rotate with each other (Endurance rides, runs). |
| `levels` | list, e.g. `[push]` | Optional. The Week Levels it may be planned in. Left out means any. |
| `alternative` | Workout `id`, or a list of them | Optional. The Alternative of similar effort, in another sport, offered next to this Endurance Workout. A list is in order of preference: `push-week` offers the first one in a tiered sport whose Equipment the profile has. The body ends with a matching `Alternative: swap this for …` line, which is not pushed. |
| `dose` | `{light: "...", normal: "...", push: "..."}` | Optional. The Workout's Dose at each Week Level. Not set on any Workout yet. Composed strength takes its rounds from the Level (picking rule 6), and composed mobility is 2 rounds at every Level (picking rule 9). |

Run Workouts write their pace as `{easy_run_pace}` or `{threshold_run_pace}`, filled from the Athlete Profile when they're pushed. Run Quality targets are threshold pace plus an offset, with an RPE alongside for hills, wind and bad days:

| Run zone | Pace | RPE |
|----------|------|-----|
| Tempo | `{threshold_run_pace}` +15–20 s/km | 6/10 |
| Threshold | `{threshold_run_pace}` ±5 s/km | 7–8/10 |
| VO2max | `{threshold_run_pace}` −10–15 s/km | 8–9/10 |

## Exercises

A single strength or mobility movement (ADR 0004). Strength Sessions and Strength Add-ons have no Workout of their own: each Check-in composes them from Exercises, and the Week Plan lists the Exercise IDs. Mobility Sessions are composed from `mobility` Exercises too, or use a whole `kind: mobility` Workout (picking rule 9). Exercise IDs share one namespace with Workout IDs, so no two files may use the same `id`.

An Exercise is recognised by its folder alone: every file in an `exercises/` folder (`bank/exercises/`, `athlete/bank/exercises/`) is an Exercise, and every file elsewhere is a Workout. A file outside `exercises/` that has a `pattern` fails the mechanical checks with "Exercises go in exercises/".

| Field | Value | Meaning |
|-------|-------|---------|
| `id` | lowercase, dashes | The name used in Week Records. Same as the file name. |
| `name` | string | How the move is listed in the pushed note. |
| `pattern` | `squat` \| `hinge` \| `push` \| `pull` \| `carry` \| `core` \| `mobility` | The movement pattern, for balancing the week (picking rule 6). |
| `equipment` | list of tags | As for Workouts: every tag must be at the day's Place. Band moves that need a door or post to pull against also carry `band-anchor`. |
| `reps` or `hold` | string, e.g. `"10"`, `"8/side"`, `"30 s"` | The amount per round. Exactly one of the two. |

The body is one or two cue lines, then a `Progress:` line. The cue is pushed next to the move. The Progress line is for the athlete and the Check-in, and isn't pushed.

```markdown
---
id: kb-goblet-squat
name: Goblet squat (kettlebell)
pattern: squat
equipment: [kettlebell]
reps: "10"
---

Hold the bell at your chest and sit down between your heels, 3 s on the way down.

Progress: more reps (up to 15), then a 2 s pause at the bottom.
```

## Personal Workouts and Exercises

This folder is the **Core Bank**. The athlete's own **Personal Workouts and Exercises** live in their athlete repo, in the same file format: Exercises in `athlete/bank/exercises/`, Workouts in `athlete/bank/workouts/` (ADR 0005). `icu.py` loads both parts as one Workout Bank. They share one ID namespace, and an ID in both parts is an error, never an override. Add one with `/add-workout`.

Every Bank file, Core or Personal, must pass the mechanical checks, or `icu.py` refuses to load the Bank and names the file. Run `./scripts/icu.py check-bank` to check them:
- the required fields are present: `id`, `name`, `kind`, `sport`, `duration_min`, `equipment` and `delivery` for a Workout; `id`, `name`, `pattern`, `equipment` and exactly one of `reps` or `hold` for an Exercise;
- `kind`, `sport`, `pattern` and `delivery` take the values in the tables above, and every `equipment` tag is a known one;
- `id` is the file name;
- a `delivery: workout` file has an `intervals` block, and a `quality` Workout has `ladder` and `step`;
- every `alternative` is in the Bank.

## Principles checklist

Apply it, out loud, whenever a Workout or Exercise is added, Core or Personal. Fix whatever fails, or explain why it stands.

- Its kind, sport and Equipment are honest: it needs exactly what it lists.
- Rides use %FTP, simple steps and repeats, and no ramps or cadence (ADR 0001). Runs use the pace placeholders (`{easy_run_pace}`, `{threshold_run_pace}`) plus RPE.
- Quality Workouts sit on a Ladder step, and are only planned as Quality.
- Strength and mobility Exercises have one pattern, a cue and a `Progress:` line.
- Nothing is meant to be paired with a Quality Session.
- It's safe for the athlete's stated injuries and Notes.
- It's foundational and functional rather than novel. For Core files: widely applicable.
- Its length fits the Level ranges (picking rule 4), or it has `levels` set.

`other` activities skip the checklist: their content isn't the athlete's to define, so they stay in the profile's `other`.

## Index

### Quality: ride Ladders

| Step | Sweet Spot | Threshold | VO2max |
|------|------------|-----------|--------|
| 1 | [ss-1](quality/ss-1.md) 3×8′ @ 88% · 54′ | [th-1](quality/th-1.md) 4×5′ @ 97% · 53′ | [vo2-1](quality/vo2-1.md) 5×2′ @ 110% · 50′ |
| 2 | [ss-2](quality/ss-2.md) 3×10′ @ 88% · 60′ | [th-2](quality/th-2.md) 3×8′ @ 97% · 57′ | [vo2-2](quality/vo2-2.md) 5×3′ @ 110% · 55′ |
| 3 | [ss-3](quality/ss-3.md) 3×12′ @ 90% · 66′ | [th-3](quality/th-3.md) 3×10′ @ 97% · 66′ | [vo2-3](quality/vo2-3.md) 6×3′ @ 112% · 61′ |
| 4 | [ss-4](quality/ss-4.md) 2×18′ @ 90% · 64′ | [th-4](quality/th-4.md) 2×20′ @ 95% · 73′ | [vo2-4](quality/vo2-4.md) 5×4′ @ 110% · 60′ |
| 5 | [ss-5](quality/ss-5.md) 2×20′ @ 92% · 68′ | | |

### Quality: run Ladders

Pushed as notes. Each has a 15′ easy warm-up with strides and a 10′ easy cool-down. Run Tempo plays Sweet Spot's role in the picking rules.

| Step | Tempo | Threshold | VO2max |
|------|-------|-----------|--------|
| 1 | [run-tempo-1](quality/run-tempo-1.md) 3×6′ · 47′ | [run-th-1](quality/run-th-1.md) 4×5′ · 51′ | [run-vo2-1](quality/run-vo2-1.md) 6×2′ · 47′ |
| 2 | [run-tempo-2](quality/run-tempo-2.md) 3×8′ · 53′ | [run-th-2](quality/run-th-2.md) 3×8′ · 53′ | [run-vo2-2](quality/run-vo2-2.md) 5×3′ · 52′ |
| 3 | [run-tempo-3](quality/run-tempo-3.md) 2×12′ · 52′ | [run-th-3](quality/run-th-3.md) 3×10′ · 61′ | [run-vo2-3](quality/run-vo2-3.md) 6×3′ · 58′ |
| 4 | [run-tempo-4](quality/run-tempo-4.md) 2×15′ · 58′ | [run-th-4](quality/run-th-4.md) 2×15′ · 58′ | [run-vo2-4](quality/run-vo2-4.md) 5×4′ · 57′ |

**Run test:** [run-test-20](test/run-test-20.md), a 20′ time trial (about 50′ with warm-up and cool-down). Its average pace is the new `threshold_run_pace`.

### Endurance

Alternatives are listed in order of preference: the first one the profile can use is offered (a tiered sport, and the Equipment it needs at any one Place: an Alternative is a swap on the day).

| Ride | Min | Alternatives | Levels |
|------|-----|--------------|--------|
| [end-ride-50](endurance/end-ride-50.md) | 50 | swim-easy-1500, run-easy-6-8 | any |
| [end-ride-50-rolling](endurance/end-ride-50-rolling.md) | 50 | swim-drills-1800, run-easy-6-8 | any |
| [end-ride-50-steps](endurance/end-ride-50-steps.md) | 50 | swim-easy-1500, run-easy-6-8 | any |
| [end-ride-60](endurance/end-ride-60.md) | 60 | run-easy-8-10, swim-steady-2000 | any |
| [end-ride-60-rolling](endurance/end-ride-60-rolling.md) | 60 | run-easy-8-10, swim-steady-2000 | any |
| [end-ride-60-steps](endurance/end-ride-60-steps.md) | 60 | run-easy-8-10, swim-steady-2000 | any |
| [end-ride-60-openers](endurance/end-ride-60-openers.md) | 60 | run-easy-strides, swim-drills-1800 | any |
| [end-ride-75](endurance/end-ride-75.md) | 75 | run-easy-8-10, swim-steady-2500 | Normal, Push |
| [end-ride-75-progressive](endurance/end-ride-75-progressive.md) | 75 | run-easy-10-12, swim-steady-2500 | Push |

| Run | Min | Alternatives | Levels |
|-----|-----|--------------|--------|
| [run-easy-5-6](endurance/run-easy-5-6.md) | 38 | end-ride-50, swim-easy-1500 | any |
| [run-easy-6-8](endurance/run-easy-6-8.md) | 45 | end-ride-50, swim-drills-1800 | any |
| [run-easy-strides](endurance/run-easy-strides.md) | 48 | end-ride-50-rolling, swim-drills-1800 | any |
| [run-easy-8-10](endurance/run-easy-8-10.md) | 55 | end-ride-60, swim-steady-2000 | any |
| [run-easy-10-12](endurance/run-easy-10-12.md) | 68 | end-ride-75, swim-steady-2500 | Push (the long run) |

Runs are at easy pace (`{easy_run_pace}` from the Athlete Profile).

| Swim | Metres | Min | Alternatives | Levels |
|------|--------|-----|--------------|--------|
| [swim-easy-1500](endurance/swim-easy-1500.md) | 1500 | 35 | run-easy-5-6, end-ride-50 | any |
| [swim-drills-1800](endurance/swim-drills-1800.md) | 1800 | 40 | end-ride-50, run-easy-6-8 | any |
| [swim-steady-2000](endurance/swim-steady-2000.md) | 2000 | 45 | end-ride-60, run-easy-6-8 | any |
| [swim-steady-2500](endurance/swim-steady-2500.md) | 2500 | 55 | end-ride-60, run-easy-8-10 | Normal, Push |

Swims need a `pool` and are pushed as notes. Each is a warm-up, drills, a main set by distance and feel (easy RPE 3–4/10, steady 5/10) and a cool-down. There are no swim Ladders yet.

### Strength, mobility, recovery, test

- **Strength Sessions** and **Strength Add-ons** are composed from the Exercises below (picking rule 6). A Strength Session of 5–6 Exercises is about 30–40′; an Add-on of 2–3 is 12–15′, after an Endurance Session or a Test Session's spin only.
- **Mobility Sessions** (~30′) come from the whole Bank, Core and Personal (picking rule 9). The Core Bank has no mobility Workout: a routine of your own, such as a physical-therapy routine, is a Personal Workout with `kind: mobility` and `sport: mobility` (`/add-workout`).
- **Recovery:** [rec-walk](recovery/rec-walk.md), a 30–60′ walk. A Recovery Day is a Mobility Session, a walk, rest or a recovery-type `other` activity, never a ride (picking rule 8).
- **FTP test:** [ftp-ramp-test](test/ftp-ramp-test.md), the MyWhoosh Ramp Test (a calendar note pointing to MyWhoosh, not a pushed workout), then [test-spin](test/test-spin.md), a 20′ easy spin. Without a smart trainer there's no Core FTP test: add your own as a Personal test Workout (picking rule 7).

### Exercises

By pattern and Equipment set. `*` marks a band move that also needs `band-anchor`. Gym moves list their tags (`barbell`, `bench`, `cable`, `pull-up-bar`); a gym Place usually lists dumbbells and kettlebells too, so their carries serve there. `mobility` Exercises are listed after the table.

| Pattern | Bodyweight | Bands | Kettlebell | Dumbbells | Gym |
|---|---|---|---|---|---|
| squat | [air-squat](exercises/air-squat.md)<br>[reverse-lunge](exercises/reverse-lunge.md)<br>[wall-sit](exercises/wall-sit.md) | [band-split-squat](exercises/band-split-squat.md)<br>[band-squat](exercises/band-squat.md) | [kb-goblet-squat](exercises/kb-goblet-squat.md)<br>[kb-split-squat](exercises/kb-split-squat.md)<br>[kb-step-up](exercises/kb-step-up.md) | [db-goblet-squat](exercises/db-goblet-squat.md)<br>[db-reverse-lunge](exercises/db-reverse-lunge.md)<br>[db-split-squat](exercises/db-split-squat.md) | [back-squat](exercises/back-squat.md)<br>[front-squat](exercises/front-squat.md) |
| hinge | [glute-bridge](exercises/glute-bridge.md)<br>[glute-bridge-march](exercises/glute-bridge-march.md)<br>[single-leg-glute-bridge](exercises/single-leg-glute-bridge.md)<br>[superman-hold](exercises/superman-hold.md) | [band-good-morning](exercises/band-good-morning.md)<br>[band-pull-through](exercises/band-pull-through.md)*<br>[banded-glute-bridge](exercises/banded-glute-bridge.md) | [kb-rdl](exercises/kb-rdl.md)<br>[kb-single-leg-rdl](exercises/kb-single-leg-rdl.md)<br>[kb-swing](exercises/kb-swing.md) | [db-glute-bridge](exercises/db-glute-bridge.md)<br>[db-rdl](exercises/db-rdl.md)<br>[db-single-leg-rdl](exercises/db-single-leg-rdl.md) | [barbell-rdl](exercises/barbell-rdl.md)<br>[deadlift](exercises/deadlift.md) |
| push | [pike-push-up](exercises/pike-push-up.md)<br>[push-up](exercises/push-up.md) | [band-chest-press](exercises/band-chest-press.md)*<br>[band-overhead-press](exercises/band-overhead-press.md) | [kb-clean-press](exercises/kb-clean-press.md)<br>[kb-floor-press](exercises/kb-floor-press.md) | [db-floor-press](exercises/db-floor-press.md)<br>[db-overhead-press](exercises/db-overhead-press.md) | [bench-press](exercises/bench-press.md) (barbell+bench)<br>[db-bench-press](exercises/db-bench-press.md) (dumbbells+bench)<br>[overhead-press](exercises/overhead-press.md) |
| pull | [prone-pulldown](exercises/prone-pulldown.md)<br>[prone-ytw](exercises/prone-ytw.md) | [band-bent-over-row](exercises/band-bent-over-row.md)<br>[band-face-pull](exercises/band-face-pull.md)*<br>[band-pull-apart](exercises/band-pull-apart.md)<br>[band-row](exercises/band-row.md)* | [kb-high-pull](exercises/kb-high-pull.md)<br>[kb-row](exercises/kb-row.md) | [db-reverse-fly](exercises/db-reverse-fly.md)<br>[db-row](exercises/db-row.md) | [barbell-row](exercises/barbell-row.md)<br>[cable-row](exercises/cable-row.md)<br>[pull-up](exercises/pull-up.md) |
| carry | [bear-crawl](exercises/bear-crawl.md) | – | [kb-rack-carry](exercises/kb-rack-carry.md)<br>[kb-suitcase-carry](exercises/kb-suitcase-carry.md) | [db-overhead-carry](exercises/db-overhead-carry.md)<br>[db-suitcase-carry](exercises/db-suitcase-carry.md) | – |
| core | [bear-hold](exercises/bear-hold.md)<br>[bicycle-crunch](exercises/bicycle-crunch.md)<br>[bird-dog](exercises/bird-dog.md)<br>[dead-bug](exercises/dead-bug.md)<br>[hollow-hold](exercises/hollow-hold.md)<br>[plank-shoulder-tap](exercises/plank-shoulder-tap.md)<br>[reverse-crunch](exercises/reverse-crunch.md)<br>[side-plank](exercises/side-plank.md)<br>[side-plank-reach-through](exercises/side-plank-reach-through.md) | [band-woodchop](exercises/band-woodchop.md)*<br>[pallof-press](exercises/pallof-press.md)* | [kb-halo](exercises/kb-halo.md)<br>[kb-russian-twist](exercises/kb-russian-twist.md) | [db-russian-twist](exercises/db-russian-twist.md)<br>[db-woodchop](exercises/db-woodchop.md) | [cable-pallof-press](exercises/cable-pallof-press.md)<br>[hanging-knee-raise](exercises/hanging-knee-raise.md) |

**Mobility,** held for time or done as slow reps:

| Area | Bodyweight | Bands |
|---|---|---|
| hips | [hip-90-90](exercises/hip-90-90.md)<br>[couch-stretch](exercises/couch-stretch.md)<br>[pigeon-stretch](exercises/pigeon-stretch.md)<br>[deep-squat-hold](exercises/deep-squat-hold.md)<br>[worlds-greatest-stretch](exercises/worlds-greatest-stretch.md)<br>[leg-swing](exercises/leg-swing.md) | – |
| thoracic spine | [cat-cow](exercises/cat-cow.md)<br>[thread-the-needle](exercises/thread-the-needle.md)<br>[open-book](exercises/open-book.md) | – |
| ankles | [ankle-knee-to-wall](exercises/ankle-knee-to-wall.md)<br>[calf-stretch](exercises/calf-stretch.md) | – |
| hamstrings | [hamstring-fold](exercises/hamstring-fold.md) | [band-hamstring-stretch](exercises/band-hamstring-stretch.md) |
| shoulders | [wall-slide](exercises/wall-slide.md)<br>[puppy-stretch](exercises/puppy-stretch.md) | [band-dislocate](exercises/band-dislocate.md) |

Thin spots: a bodyweight-only profile has one carry (`bear-crawl`), and bands alone have none, so a week for those profiles covers carry with `bear-crawl` or another kit's carry.

### Old IDs

`str-a/b/c` and `addon-core/upper/posterior` are retired (ADR 0004). Week Records that name them stay as they are. Their moves are now these Exercises:

| Old ID | Exercises |
|--------|-----------|
| `str-a` | kb-swing, kb-goblet-squat, band-row, push-up, dead-bug; finisher plank-shoulder-tap, hollow-hold, glute-bridge-march; warm-up air-squat |
| `str-b` | kb-split-squat, kb-single-leg-rdl, kb-floor-press, band-pull-apart, side-plank; finisher bear-hold, reverse-crunch, bicycle-crunch; warm-up reverse-lunge, glute-bridge |
| `str-c` | kb-suitcase-carry, kb-clean-press, kb-step-up, band-face-pull, pallof-press; finisher side-plank-reach-through, bird-dog, kb-russian-twist; warm-up kb-halo |
| `addon-core` | dead-bug, bird-dog, side-plank, pallof-press |
| `addon-upper` | band-row, push-up, band-pull-apart, kb-halo, band-face-pull |
| `addon-posterior` | kb-swing, banded-glute-bridge, kb-rdl, superman-hold |

The Core `pt` Workout (`kind: pt`, `sport: pt`) is retired too, with the `pt` tier, which is now `mobility`. A PT routine is now a Personal mobility Workout (the maintainer's keeps the ID `pt`, in `athlete/bank/workouts/pt.md`), or a Mobility Session is composed from the mobility Exercises above (picking rule 9).

## Picking rules (used by the Check-in)

1. **Quality pairing:** applies to each Primary sport that has Ladders (ride and run), using the Quality slots the Week Template gives it (generation rule 2 in `docs/planning-rules.md`):
   - **Two slots** (the only such sport): the first Quality day of the week alternates week to week between the **Threshold** and **VO2max** Ladders. The second is always **Sweet Spot**. In the maintainer's template that's Tuesday and Thursday.
   - **One slot** (two or three such sports): the slot rotates week to week, Sweet Spot → Threshold → VO2max.
   - **Light week:** the one Quality slot is either Endurance or one Sweet Spot Workout a step *below* your current step.
   - **Run:** run Tempo plays Sweet Spot's role, so a run's two-slot pattern is Threshold or VO2max, then Tempo; its one-slot rotation is Tempo → Threshold → VO2max; and a Light run slot is Endurance or a Tempo step below.
2. **Climbing:**
   - Completed at an effort of 7/10 or below: next step.
   - 8/10, or one rep cut short: repeat the same step.
   - Two failed attempts in a row: drop a step.
   - After a Light week: stay on the same step.
   - After a retest (the FTP test for ride, the run test for run): drop one step on every Ladder of that sport, because the targets just got harder.
   - Top step completed at 7/10 or below: hold there and bring that sport's next test forward.
3. **Starting steps:** set by `experience`, on every Ladder of each Primary sport that has Ladders: `new` starts at step 1, `some` at step 2 (ss-2, th-2, vo2-2 for ride; run-tempo-2, run-th-2, run-vo2-2 for run), and `experienced` at step 3. This applies to run as it does to ride. If the starting step feels too hard, drop a step using rule 2.
4. **Dose by Level:** the Level picks each Workout's Dose. Endurance ride length is the first case of Dose. Each Level sets a range, not a fixed length, so vary the lengths within it, week to week and by how the athlete feels:
   - Light: 50–60′ rides.
   - Normal: 60–75′, with at most one 75′ ride (`end-ride-75`, on the template's long day, Saturday for the maintainer).
   - Push: 60–75′, with at least one 75′ ride on the long day. Either 75′ ride may be used, and both in one week.

   Endurance runs:
   - Light: 35–45′ runs.
   - Normal: 45–60′.
   - Push: 45–70′, with one long run (`run-easy-10-12`) on the long day.

   Endurance swims:
   - Light: 1500–2000 m.
   - Normal and Push: 1800–2500 m (`swim-steady-2500` is Normal or Push only).

   **Extension:** in a Push week, at most one Quality ride may get 10–15′ extra at Endurance (68%) before its cooldown, written `+<minutes>` after its ID in the Plan table (`th-2 +15`). Use it now and then, when the athlete is fresh, never in a Light or Normal week, and never on the FTP test. Quality Workouts otherwise keep the length their Ladder step gives them.

   If `alternatives: on`, every Endurance Session names an Alternative of similar effort in another tiered sport, which you can swap in on the day. `push-week` offers the first Alternative on the Workout's list that the profile can use. Where the Week Template names one (`ride (alt: swim)`), pick a Workout whose first usable Alternative is that sport: the 50′ rides offer a swim first, the other rides and the runs offer a run or ride first and a swim after it.
5. **Endurance variety:** never the same Workout twice in one week. Prefer a different Workout from the one on the same day last week.
6. **Strength:** only if strength is tiered. Compose each Strength Session and Add-on from the Exercises whose Equipment the day's Place has:
   - **Size:** aim for 5–6 Exercises in a Strength Session and 2–3 in an Add-on. `push-week` only rejects clear mistakes: a Session outside 3–8 or an Add-on outside 2–4. No Exercise twice in one row.
   - **Balance:** all the strength in the week, Sessions and Add-ons together, covers squat, hinge, push, pull, carry and core. A lone Strength Session in a week is full-body, covering all six itself. A week whose only strength is an Add-on or two (strength Occasional, say) can't hold all six: cover them over two or three weeks, starting with the patterns last week's Add-ons missed.
   - **Variety:** prefer Exercises not used last week (read last week's Plan rows), and vary between Sessions in the same week.
   - **Dose:** rounds by Level, Light 2, Normal 3, Push 4. `push-week` writes the rounds into the note, so the Plan row lists only the Exercise IDs, in order.
   - **Gap:** if no Exercise fits a pattern, cover it elsewhere in the week; if nothing in the week can, it's a gap.
7. **Tests:** each sport's test resets its Ladder targets. When due (about 6 weeks since that sport's last test, and the previous week was Light), it replaces the week's first Quality Session of that sport. After it, drop a step on that sport's Ladders, and bring it forward when a top step is done (rule 2).
   - **FTP test:** only if ride is Primary. A Test row is `ftp-ramp-test, test-spin`, optionally with an Add-on, and comes to about 60–75′. Without a smart trainer the Core Bank has no FTP test: a Personal `kind: test`, `sport: ride` Workout (an outdoor 20′ test, say, added with `/add-workout`) takes its place, alone or followed by `test-spin`.
   - **Run test:** only if run is Primary. A Test row is `run-test-20` alone, about 50′. Not in the same week as the FTP test.
8. **Walk:** for Recovery Days the template gives a walk, or as a stand-in on the day for any Session when you're too tired. Never a recovery ride.
9. **Mobility:** only if mobility is tiered. A Mobility Session is one of these, from Core and Personal alike:
   - a whole `kind: mobility` Workout (such as a physical-therapy routine kept as a Personal Workout);
   - 6–8 composed `mobility` Exercises whose Equipment the day's Place has;
   - a whole `kind: mobility` Workout followed by 2–3 mobility Exercises.

   It's one activity, so the last isn't a Pairing.

   **Dose:** composed mobility is 2 rounds at every Level, Light, Normal and Push alike: mobility Exercises are held for time or done as slow reps, for maintenance, so the Level changes the strength rounds and the training days, never the mobility. `push-week` pushes a composed block as one note, "Mobility (2 rounds)", moving slowly between the holds.

   Vary the mix across the week, following any preference in the profile's Notes ("PT most days, Bank mobility now and then"): nothing in the profile locks a routine in. Prefer mobility Exercises not used last week, and cover hips, thoracic spine, ankles, hamstrings and shoulders across the week. With `mobility+strength` in `pairings`, a Mobility Session may come before a Strength Session in one row: a mobility block and a strength block are separate notes even when their Exercise IDs are adjacent.
