---
tiers:
  pt: primary
  strength: secondary
  walk: occasional
other:
  - {id: pilates, name: "Pilates class", minutes: 45, counts_as: training}
  - {id: yin-yoga, name: "Yin yoga video", minutes: 30, counts_as: recovery}
equipment: [bodyweight, dumbbells]
availability:
  days_per_week: 4
  fixed:
    Thu: other:pilates
pairings: [pt+strength]
setup:
  sync_verified: no
  strava_connected: no
---

# Athlete Profile

An invented example: someone training at home, built around a PT routine, with bodyweight and one dumbbell, a weekly Pilates class and four training days. No ride, run or swim, so no Quality Sessions, FTP, heart rate or run pace. Your own profile lives in `athlete/profile.md`. The format is in `docs/athlete-profile.md`.

## Week Templates

| Day | Light | Normal | Push |
|-----|-------|--------|------|
| Mon | Strength: pt, strength | Strength: pt, strength | Strength: pt, strength |
| Tue | Recovery: pt | Recovery: pt | Other: other:pilates |
| Wed | Recovery: walk | Recovery: walk | Recovery: pt |
| Thu | Other: other:pilates | Other: other:pilates | Other: other:pilates |
| Fri | Recovery: pt | Strength: pt, strength | Strength: pt, strength |
| Sat | Recovery: other:yin-yoga | Recovery: pt | Recovery: walk |
| Sun | Recovery: rest | Recovery: rest | Recovery: other:yin-yoga or rest |

How the rules in `docs/planning-rules.md` were applied:
- **Training days:** 2 (Light), 3 (Normal) and 4 (Push). Thursday's Pilates class is fixed and placed first.
- **Quality:** none. No Primary sport has Ladders.
- **Tiers:** PT, Primary, is on at least 2 days at every Level, paired before strength as the profile allows. Strength, Secondary, is on 1 day in Light and 2 in Normal and Push. The walk, Occasional, is on 1 day.
- **Push:** strength is capped at 2 days as a Secondary activity, so the fourth training day is a second Pilates Session on Tuesday.
- **Dose:** the Level sets the rounds of each strength and PT Workout.

## Notes

- PT and walks count as Recovery Days. The training days here are strength and Pilates.
- Gaps found at Setup (for the Bank, item 3):
  - **No dumbbell or bodyweight Strength Workouts.** `str-a`, `str-b` and `str-c` all use a kettlebell, so Strength Sessions can't be filled yet.
