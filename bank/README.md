# Workout Bank

The curated set of Workouts every Week Plan draws from (see `GLOSSARY.md`). There's one file per Workout. The frontmatter holds the fields the Check-in uses to pick Workouts. Ride bodies hold an `intervals` block (intervals.icu workout text) that is pushed to intervals.icu and synced to MyWhoosh.

Ride targets are **%FTP** with simple steps and repeats, and no ramps or cadence targets (ADR 0001). Example watts at FTP 240:

| Zone | %FTP | Watts |
|------|------|-------|
| Endurance (Zone 2) | 62–74% | 150–178 W |
| Sweet Spot | 88–92% | 211–221 W |
| Threshold | 95–97% | 228–233 W |
| VO2max | 110–112% | 264–269 W |

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

| Ride | Min | Run alternative | Levels |
|------|-----|-----------------|--------|
| [end-ride-50](endurance/end-ride-50.md) | 50 | run-easy-6-8 | any |
| [end-ride-50-rolling](endurance/end-ride-50-rolling.md) | 50 | run-easy-6-8 | any |
| [end-ride-50-steps](endurance/end-ride-50-steps.md) | 50 | run-easy-6-8 | any |
| [end-ride-60](endurance/end-ride-60.md) | 60 | run-easy-8-10 | any |
| [end-ride-60-rolling](endurance/end-ride-60-rolling.md) | 60 | run-easy-8-10 | any |
| [end-ride-60-steps](endurance/end-ride-60-steps.md) | 60 | run-easy-8-10 | any |
| [end-ride-60-openers](endurance/end-ride-60-openers.md) | 60 | run-easy-strides | any |
| [end-ride-75](endurance/end-ride-75.md) | 75 | run-easy-10-12 | Push |
| [end-ride-75-progressive](endurance/end-ride-75-progressive.md) | 75 | run-easy-10-12 | Push |

Runs (easy pace, 5:45–6:00/km in the run files; change it to your own):
- [run-easy-6-8](endurance/run-easy-6-8.md), ~45′
- [run-easy-8-10](endurance/run-easy-8-10.md), ~55′
- [run-easy-10-12](endurance/run-easy-10-12.md), ~68′, Push weeks only
- [run-easy-strides](endurance/run-easy-strides.md), ~48′

### Strength, PT, recovery, test

- **Strength Sessions** (~33′ including a 5′ core finisher, after PT on Monday, so Monday is about 60′ in total):
  - [str-a](strength/str-a.md): hinge and push
  - [str-b](strength/str-b.md): single leg
  - [str-c](strength/str-c.md): carry and core
- **Strength Add-ons** (12–15′, after an Endurance Session only):
  - [addon-core](add-ons/addon-core.md)
  - [addon-upper](add-ons/addon-upper.md)
  - [addon-posterior](add-ons/addon-posterior.md)
- **PT:** [pt](pt/pt.md), ~30′; contents are your own routine.
- **Recovery:** [rec-walk](recovery/rec-walk.md), a 30–60′ walk. Recovery Days are always off the bike, so there's no trainer setup.
- **FTP test:** [ftp-ramp-test](test/ftp-ramp-test.md), the MyWhoosh Ramp Test (a calendar note pointing to MyWhoosh, not a pushed workout), then [test-spin](test/test-spin.md), a 20′ easy spin.

## Picking rules (used by the Check-in)

1. **Quality pairing:** Tuesday alternates week to week between the **Threshold** and **VO2max** Ladders. Thursday is always **Sweet Spot**. In a Light week, Tuesday is either Endurance or one Sweet Spot Workout a step *below* your current step.
2. **Climbing:**
   - Completed at an effort of 7/10 or below: next step.
   - 8/10, or one rep cut short: repeat the same step.
   - Two failed attempts in a row: drop a step.
   - After a Light week: stay on the same step.
   - After an FTP retest: drop one step on every Ladder, because the targets just got harder.
   - Top step completed at 7/10 or below: hold there and bring the next FTP test forward.
3. **Starting steps:** ss-2, th-2 and vo2-2. You've been riding structured workouts, so step 1 is skipped. If step 2 feels too hard, drop to step 1 using rule 2.
4. **Endurance length by Level:**
   - Light: 50′ rides.
   - Normal: 60′.
   - Push: 60′, plus 75′ on Saturday.

   Every Endurance ride names a run alternative of similar effort, which you can swap in on the day.
5. **Endurance variety:** never the same Workout twice in one week. Prefer a different Workout from the one on the same day last week.
6. **Strength:** Monday cycles A → B → C. The Wednesday Add-on cycles core → upper → posterior.
7. **FTP test:** when due (about 6 weeks since the last test, and the previous week was Light), it replaces Tuesday's Quality Session. A Test row is `ftp-ramp-test, test-spin`, optionally with an Add-on, and comes to about 60–75′.
8. **Walk:** for Light-week Sundays, or as a stand-in on the day for any Session when you're too tired. Never a recovery ride.
