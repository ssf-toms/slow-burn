---
tiers:
  strength: primary
  run: secondary
  walk: occasional
other: []
places:
  home: [bodyweight, dumbbells]
  gym: [barbell, bench, cable, pull-up-bar, dumbbells, kettlebell]
availability:
  days_per_week: 5
  fixed:
    Wed: strength @gym
easy_run_pace: "6:00–6:30/km"
pairings: []
setup:
  sync_verified: no
  strava_connected: yes
---

# Athlete Profile

An invented example: someone who lifts at home with bodyweight and a pair of dumbbells, goes to the gym every Wednesday, and runs. Two Places: home, the default, and the gym. Your own profile lives in `athlete/profile.md`. The format is in `docs/athlete-profile.md`.

## Week Templates

| Day | Light | Normal | Push |
|-----|-------|--------|------|
| Mon | Strength: strength | Strength: strength | Strength: strength |
| Tue | Recovery: walk | Recovery: rest | Endurance: run |
| Wed | Strength: strength @gym | Strength: strength @gym | Strength: strength @gym |
| Thu | Recovery: rest | Recovery: walk | Recovery: walk |
| Fri | Recovery: rest | Strength: strength | Strength: strength |
| Sat | Endurance: run | Endurance: run | Endurance: run |
| Sun | Recovery: rest | Recovery: rest | Recovery: rest |

How the rules in `docs/planning-rules.md` were applied:
- **Fixed days:** Wednesday's gym strength is placed first, marked `@gym`. Every other day is at home, the default Place.
- **Training days:** 3 (Light), 4 (Normal) and 5 (Push).
- **Quality:** none. Run is Secondary, and only a Primary sport with Ladders gets Quality slots.
- **Tiers:** strength, Primary, is on at least 2 days at every Level: Monday at home and Wednesday at the gym, plus Friday at home in Normal and Push. Run, Secondary, is on 1 day, 2 in Push. The walk, Occasional, is on 1 day.
- **Dose:** the Level sets the rounds of each Strength Session and the length of each run.

## Notes

- Home Strength Sessions are composed from the bodyweight and dumbbell Exercises, the gym one from the barbell, cable and pull-up bar Exercises as well. Both cover every pattern.
- No Bank gaps.
