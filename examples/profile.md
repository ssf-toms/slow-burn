---
tiers:
  ride: primary
  run: primary
  swim: secondary
  strength: occasional
other: []
places:
  home: [bodyweight, bands, hr-strap]
  gym: [pool, hr-strap]
experience: some
availability:
  days_per_week: 6
  fixed:
    Mon: rest
easy_run_pace: "5:20–5:40/km"
threshold_run_pace: "4:50/km"
alternatives: on
ftp: 230
lthr: 168
max_hr: 186
setup:
  sync_verified: no
  strava_connected: yes
---

# Athlete Profile

An invented example: a triathlete who rides outdoors (no smart trainer), runs, swims at their gym's pool, and trains six days a week. Two Places: home, the default, and the gym, used only for its pool. Your own profile lives in `athlete/profile.md`. The format is in `docs/athlete-profile.md`.

## Week Templates

| Day | Light | Normal | Push |
|-----|-------|--------|------|
| Mon | Recovery: rest | Recovery: rest | Recovery: rest |
| Tue | Quality: ride or run | Quality: ride | Quality: ride |
| Wed | Endurance: run or ride | Endurance: ride (alt: run) + Add-on | Endurance: ride (alt: run) + Add-on |
| Thu | Recovery: rest | Quality: run | Quality: run |
| Fri | Endurance: ride (alt: swim) | Recovery: rest | Endurance: swim @gym |
| Sat | Recovery: rest | Endurance: swim @gym | Endurance: ride |
| Sun | Endurance: run | Endurance: run | Endurance: run |

How the rules in `docs/planning-rules.md` were applied:
- **Training days:** 4 (Light), 5 (Normal) and 6 (Push). Monday is a fixed rest day. Walks and PT aren't tiered, so every Recovery Day is rest.
- **Quality:** ride and run are both Primary with Ladders, so each gets one slot: ride on Tuesday and run on Thursday, never consecutive. Light keeps one, on Tuesday, alternating between ride and run Light week to Light week; Wednesday is then the other sport, so both keep 2 days.
- **Tiers:** ride and run, both Primary, have at least 2 days at every Level. Swim, Secondary, has 1. Strength, Occasional, is one Add-on in Normal and Push.
- **Light:** four days can't hold two Primaries at 2 days each plus a swim, so swim is the named Alternative on Friday instead.
- **Places:** every swim is at the gym, so swim days are marked `@gym`. The rest are at home, the default. A swim Alternative on a home day is fine: it's a swap on the day.
- **Dose:** Saturday is the long day: a 75′ ride in Push, and in Normal the one ride that may go to 75′. Sunday is the long run in Push.

## Notes

- Rides are outdoors. With no `smart-trainer`, rides are pushed as outdoor and the MyWhoosh steps are skipped.
- Gaps found at Setup (for the Bank, item 3):
  - **The FTP test** (`ftp-ramp-test`) is a MyWhoosh Ramp Test, which needs a smart trainer. Ride is Primary, so a test is due, but there's no outdoor test.
  - **Strength Add-ons** are composed from the bodyweight and band Exercises (no `band-anchor`, so no Pallof press or band row). The gym Place lists only `pool`: list more of its kit (`barbell`, `dumbbells`, `cable`, …) to plan strength there.
