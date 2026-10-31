# Workout Bank

The curated set of Workouts and Exercises every Week Plan draws from (see `GLOSSARY.md`). There's one file per Workout, and one per Exercise in `exercises/`. The frontmatter holds the fields the Check-in uses to pick Workouts. Ride bodies hold an `intervals` block (intervals.icu workout text) that is pushed to intervals.icu and synced to MyWhoosh.

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
| `kind` | `quality` \| `endurance` \| `pt` \| `recovery` \| `test` | What the Workout is for. |
| `sport` | `ride` \| `run` \| `walk` \| `strength` \| `pt` | The activity. |
| `duration_min` | number | Typical length in minutes. |
| `equipment` | list of tags, `[]` for none | The Equipment the Workout needs, from the tags in `docs/athlete-profile.md` (`bodyweight`, `bands`, `band-anchor`, `kettlebell`, `dumbbells`, `barbell`, `bench`, `cable`, `pull-up-bar`, `gym`, `smart-trainer`, `pool`, `hr-strap`). It can only be planned if the athlete has every tag. The one exception: `smart-trainer` on a `delivery: workout` ride only decides whether it's pushed as indoor or outdoor, so the ride can be planned without one. Required in every file. |
| `delivery` | `workout` \| `note` | `workout` is pushed as a structured workout (rides). `note` is a calendar note. |
| `ladder`, `step` | Ladder name, number | Quality Workouts only: which Ladder, and which step on it. |
| `variant_group` | string | Workouts that rotate with each other (Endurance rides, runs). |
| `levels` | list, e.g. `[push]` | Optional. The Week Levels it may be planned in. Left out means any. |
| `alternative` | Workout `id` | Optional. The Alternative of similar effort, in another sport, offered next to this Endurance Workout. The body ends with a matching `Alternative: swap this for …` line, which is not pushed. |
| `dose` | `{light: "...", normal: "...", push: "..."}` | Optional. The Workout's Dose at each Week Level, Not set on any Workout yet. Composed strength takes its rounds from picking rule 6 instead. |

Run Workouts write their pace as `{easy_run_pace}`, which is filled from the Athlete Profile when they're pushed.

## Exercises

A single strength or mobility movement (ADR 0004). Strength Sessions and Strength Add-ons have no Workout of their own: each Check-in composes them from Exercises, and the Week Plan lists the Exercise IDs. Exercise IDs share one namespace with Workout IDs, so no two files may use the same `id`.

| Field | Value | Meaning |
|-------|-------|---------|
| `id` | lowercase, dashes | The name used in Week Records. Same as the file name. |
| `name` | string | How the move is listed in the pushed note. |
| `pattern` | `squat` \| `hinge` \| `push` \| `pull` \| `carry` \| `core` \| `mobility` | The movement pattern, for balancing the week (picking rule 6). |
| `equipment` | list of tags | As for Workouts: every tag must be in the profile's `equipment`. Band moves that need a door or post to pull against also carry `band-anchor`. |
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

## Index

### Quality: Ladders (bike only)

| Step | Sweet Spot | Threshold | VO2max |
|------|------------|-----------|--------|
| 1 | [ss-1](quality/ss-1.md) 3×8′ @ 88% · 54′ | [th-1](quality/th-1.md) 4×5′ @ 97% · 53′ | [vo2-1](quality/vo2-1.md) 5×2′ @ 110% · 50′ |
| 2 | [ss-2](quality/ss-2.md) 3×10′ @ 88% · 60′ | [th-2](quality/th-2.md) 3×8′ @ 97% · 57′ | [vo2-2](quality/vo2-2.md) 5×3′ @ 110% · 55′ |
| 3 | [ss-3](quality/ss-3.md) 3×12′ @ 90% · 66′ | [th-3](quality/th-3.md) 3×10′ @ 97% · 66′ | [vo2-3](quality/vo2-3.md) 6×3′ @ 112% · 61′ |
| 4 | [ss-4](quality/ss-4.md) 2×18′ @ 90% · 64′ | [th-4](quality/th-4.md) 2×20′ @ 95% · 73′ | [vo2-4](quality/vo2-4.md) 5×4′ @ 110% · 60′ |
| 5 | [ss-5](quality/ss-5.md) 2×20′ @ 92% · 68′ | | |

### Endurance

| Ride | Min | Alternative | Levels |
|------|-----|-----------------|--------|
| [end-ride-50](endurance/end-ride-50.md) | 50 | run-easy-6-8 | any |
| [end-ride-50-rolling](endurance/end-ride-50-rolling.md) | 50 | run-easy-6-8 | any |
| [end-ride-50-steps](endurance/end-ride-50-steps.md) | 50 | run-easy-6-8 | any |
| [end-ride-60](endurance/end-ride-60.md) | 60 | run-easy-8-10 | any |
| [end-ride-60-rolling](endurance/end-ride-60-rolling.md) | 60 | run-easy-8-10 | any |
| [end-ride-60-steps](endurance/end-ride-60-steps.md) | 60 | run-easy-8-10 | any |
| [end-ride-60-openers](endurance/end-ride-60-openers.md) | 60 | run-easy-strides | any |
| [end-ride-75](endurance/end-ride-75.md) | 75 | run-easy-10-12 | Normal, Push |
| [end-ride-75-progressive](endurance/end-ride-75-progressive.md) | 75 | run-easy-10-12 | Push |

Runs (easy pace, `{easy_run_pace}` from the Athlete Profile):
- [run-easy-6-8](endurance/run-easy-6-8.md), ~45′
- [run-easy-8-10](endurance/run-easy-8-10.md), ~55′
- [run-easy-10-12](endurance/run-easy-10-12.md), ~68′, Normal and Push weeks only
- [run-easy-strides](endurance/run-easy-strides.md), ~48′

### Strength, PT, recovery, test

- **Strength Sessions** and **Strength Add-ons** are composed from the Exercises below (picking rule 6). A Strength Session of 5–6 Exercises is about 30–40′; an Add-on of 2–3 is 12–15′, after an Endurance Session or a Test Session's spin only.
- **PT:** [pt](pt/pt.md), ~30′; contents are your own routine.
- **Recovery:** [rec-walk](recovery/rec-walk.md), a 30–60′ walk. A Recovery Day is PT, a walk, rest or a recovery-type `other` activity, never a ride (picking rule 8).
- **FTP test:** [ftp-ramp-test](test/ftp-ramp-test.md), the MyWhoosh Ramp Test (a calendar note pointing to MyWhoosh, not a pushed workout), then [test-spin](test/test-spin.md), a 20′ easy spin.

### Exercises

By pattern and Equipment set. `*` marks a band move that also needs `band-anchor`. Gym moves list their tags (`barbell`, `bench`, `cable`, `pull-up-bar`); a gym usually has dumbbells and kettlebells too, so their carries serve there. `mobility` Exercises come later.

| Pattern | Bodyweight | Bands | Kettlebell | Dumbbells | Gym |
|---|---|---|---|---|---|
| squat | [air-squat](exercises/air-squat.md)<br>[reverse-lunge](exercises/reverse-lunge.md)<br>[wall-sit](exercises/wall-sit.md) | [band-split-squat](exercises/band-split-squat.md)<br>[band-squat](exercises/band-squat.md) | [kb-goblet-squat](exercises/kb-goblet-squat.md)<br>[kb-split-squat](exercises/kb-split-squat.md)<br>[kb-step-up](exercises/kb-step-up.md) | [db-goblet-squat](exercises/db-goblet-squat.md)<br>[db-reverse-lunge](exercises/db-reverse-lunge.md)<br>[db-split-squat](exercises/db-split-squat.md) | [back-squat](exercises/back-squat.md)<br>[front-squat](exercises/front-squat.md) |
| hinge | [glute-bridge](exercises/glute-bridge.md)<br>[glute-bridge-march](exercises/glute-bridge-march.md)<br>[single-leg-glute-bridge](exercises/single-leg-glute-bridge.md)<br>[superman-hold](exercises/superman-hold.md) | [band-good-morning](exercises/band-good-morning.md)<br>[band-pull-through](exercises/band-pull-through.md)*<br>[banded-glute-bridge](exercises/banded-glute-bridge.md) | [kb-rdl](exercises/kb-rdl.md)<br>[kb-single-leg-rdl](exercises/kb-single-leg-rdl.md)<br>[kb-swing](exercises/kb-swing.md) | [db-glute-bridge](exercises/db-glute-bridge.md)<br>[db-rdl](exercises/db-rdl.md)<br>[db-single-leg-rdl](exercises/db-single-leg-rdl.md) | [barbell-rdl](exercises/barbell-rdl.md)<br>[deadlift](exercises/deadlift.md) |
| push | [pike-push-up](exercises/pike-push-up.md)<br>[push-up](exercises/push-up.md) | [band-chest-press](exercises/band-chest-press.md)*<br>[band-overhead-press](exercises/band-overhead-press.md) | [kb-clean-press](exercises/kb-clean-press.md)<br>[kb-floor-press](exercises/kb-floor-press.md) | [db-floor-press](exercises/db-floor-press.md)<br>[db-overhead-press](exercises/db-overhead-press.md) | [bench-press](exercises/bench-press.md) (barbell+bench)<br>[db-bench-press](exercises/db-bench-press.md) (dumbbells+bench)<br>[overhead-press](exercises/overhead-press.md) |
| pull | [prone-pulldown](exercises/prone-pulldown.md)<br>[prone-ytw](exercises/prone-ytw.md) | [band-bent-over-row](exercises/band-bent-over-row.md)<br>[band-face-pull](exercises/band-face-pull.md)*<br>[band-pull-apart](exercises/band-pull-apart.md)<br>[band-row](exercises/band-row.md)* | [kb-high-pull](exercises/kb-high-pull.md)<br>[kb-row](exercises/kb-row.md) | [db-reverse-fly](exercises/db-reverse-fly.md)<br>[db-row](exercises/db-row.md) | [barbell-row](exercises/barbell-row.md)<br>[cable-row](exercises/cable-row.md)<br>[pull-up](exercises/pull-up.md) |
| carry | [bear-crawl](exercises/bear-crawl.md) | – | [kb-rack-carry](exercises/kb-rack-carry.md)<br>[kb-suitcase-carry](exercises/kb-suitcase-carry.md) | [db-overhead-carry](exercises/db-overhead-carry.md)<br>[db-suitcase-carry](exercises/db-suitcase-carry.md) | – |
| core | [bear-hold](exercises/bear-hold.md)<br>[bicycle-crunch](exercises/bicycle-crunch.md)<br>[bird-dog](exercises/bird-dog.md)<br>[dead-bug](exercises/dead-bug.md)<br>[hollow-hold](exercises/hollow-hold.md)<br>[plank-shoulder-tap](exercises/plank-shoulder-tap.md)<br>[reverse-crunch](exercises/reverse-crunch.md)<br>[side-plank](exercises/side-plank.md)<br>[side-plank-reach-through](exercises/side-plank-reach-through.md) | [band-woodchop](exercises/band-woodchop.md)*<br>[pallof-press](exercises/pallof-press.md)* | [kb-halo](exercises/kb-halo.md)<br>[kb-russian-twist](exercises/kb-russian-twist.md) | [db-russian-twist](exercises/db-russian-twist.md)<br>[db-woodchop](exercises/db-woodchop.md) | [cable-pallof-press](exercises/cable-pallof-press.md)<br>[hanging-knee-raise](exercises/hanging-knee-raise.md) |

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

## Picking rules (used by the Check-in)

1. **Quality pairing:** applies to each Primary sport that has Ladders (today, only ride), using the Quality slots the Week Template gives it (generation rule 2 in `docs/planning-rules.md`):
   - **Two slots** (the only such sport): the first Quality day of the week alternates week to week between the **Threshold** and **VO2max** Ladders. The second is always **Sweet Spot**. In the maintainer's template that's Tuesday and Thursday.
   - **One slot** (two or three such sports): the slot rotates week to week, Sweet Spot → Threshold → VO2max.
   - **Light week:** the one Quality slot is either Endurance or one Sweet Spot Workout a step *below* your current step.
2. **Climbing:**
   - Completed at an effort of 7/10 or below: next step.
   - 8/10, or one rep cut short: repeat the same step.
   - Two failed attempts in a row: drop a step.
   - After a Light week: stay on the same step.
   - After an FTP retest: drop one step on every Ladder, because the targets just got harder.
   - Top step completed at 7/10 or below: hold there and bring the next FTP test forward.
3. **Starting steps:** set by `experience`, on every Ladder of each Primary sport that has Ladders: `new` starts at step 1, `some` at step 2 (ss-2, th-2, vo2-2), and `experienced` at step 3. If the starting step feels too hard, drop a step using rule 2.
4. **Dose by Level:** the Level picks each Workout's Dose. Endurance ride length is the first case of Dose. Each Level sets a range, not a fixed length, so vary the lengths within it, week to week and by how the athlete feels:
   - Light: 50–60′ rides.
   - Normal: 60–75′, with at most one 75′ ride (`end-ride-75`, on the template's long day, Saturday for the maintainer).
   - Push: 60–75′, with at least one 75′ ride on the long day. Either 75′ ride may be used, and both in one week.

   **Extension:** in a Push week, at most one Quality ride may get 10–15′ extra at Endurance (68%) before its cooldown, written `+<minutes>` after its ID in the Plan table (`th-2 +15`). Use it now and then, when the athlete is fresh, never in a Light or Normal week, and never on the FTP test. Quality Workouts otherwise keep the length their Ladder step gives them.

   If `alternatives: on`, every Endurance Session names an Alternative of similar effort in another tiered sport, which you can swap in on the day.
5. **Endurance variety:** never the same Workout twice in one week. Prefer a different Workout from the one on the same day last week.
6. **Strength:** only if strength is tiered. Compose each Strength Session and Add-on from the Exercises whose Equipment the profile has:
   - **Size:** a Strength Session has 5–6 Exercises, an Add-on 2–3. (`push-week` accepts 3–8 and 2–4.) No Exercise twice in one row.
   - **Balance:** all the strength in the week, Sessions and Add-ons together, covers squat, hinge, push, pull, carry and core. A lone Strength Session in a week is full-body, covering all six itself.
   - **Variety:** prefer Exercises not used last week (read last week's Plan rows), and vary between Sessions in the same week.
   - **Dose:** rounds by Level, Light 2, Normal 3, Push 4. `push-week` writes the rounds into the note, so the Plan row lists only the Exercise IDs, in order.
   - **Gap:** if no Exercise fits a pattern, cover it elsewhere in the week; if nothing in the week can, it's a gap.
7. **FTP test:** only if ride is Primary. When due (about 6 weeks since the last test, and the previous week was Light), it replaces the week's first ride Quality Session. A Test row is `ftp-ramp-test, test-spin`, optionally with an Add-on, and comes to about 60–75′.
8. **Walk:** for Recovery Days the template gives a walk, or as a stand-in on the day for any Session when you're too tired. Never a recovery ride.
