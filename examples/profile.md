---
tiers:
  ride: primary
  run: primary
  swim: secondary
  strength: occasional
other: []
equipment: [bodyweight, bands, gym, pool, hr-strap]
experience: some
availability:
  days_per_week: 6
  fixed:
    Mon: rest
easy_run_pace: "5:20–5:40/km"
alternatives: on
ftp: 230
lthr: 168
max_hr: 186
setup:
  sync_verified: no
  strava_connected: yes
---

# Athlete Profile

An invented example: a triathlete who rides outdoors (no smart trainer), runs, swims at their gym's pool, and trains six days a week. Your own profile lives in `athlete/profile.md`. The format is in `docs/athlete-profile.md`.

## Week Templates

| Day | Light | Normal | Push |
|-----|-------|--------|------|
| Mon | Recovery: rest | Recovery: rest | Recovery: rest |
| Tue | Quality: ride | Quality: ride | Quality: ride |
| Wed | Endurance: run | Endurance: run + Add-on | Endurance: run + Add-on |
| Thu | Recovery: rest | Quality: ride | Quality: ride |
| Fri | Endurance: ride (alt: swim) | Recovery: rest | Endurance: swim |
| Sat | Recovery: rest | Endurance: swim | Endurance: ride |
| Sun | Endurance: run | Endurance: run | Endurance: run |

How the rules in `docs/planning-rules.md` were applied:
- **Training days:** 4 (Light), 5 (Normal) and 6 (Push). Monday is a fixed rest day. Walks and PT aren't tiered, so every Recovery Day is rest.
- **Quality:** ride is the only Primary sport with Ladders, so it gets both slots (Tuesday and Thursday, never consecutive). Light keeps one.
- **Tiers:** ride and run, both Primary, have at least 2 days at every Level (in Normal, ride gets its 2 from the Quality slots). Swim, Secondary, has 1. Strength, Occasional, is one Add-on in Normal and Push.
- **Light:** four days can't hold two Primaries at 2 days each plus a swim, so swim is the named Alternative on Friday instead.
- **Dose:** Saturday's Push ride is the long one (75′).

## Notes

- Rides are outdoors. With no `smart-trainer`, rides are pushed as outdoor and the MyWhoosh steps are skipped.
- Gaps found at Setup (for the Bank, item 3):
  - **No swim Workouts** in the Bank yet, so swim Sessions and the swim Alternative can't be filled.
  - **No run Ladders,** so run is Primary but gets no Quality slot.
  - **The FTP test** (`ftp-ramp-test`) is a MyWhoosh Ramp Test, which needs a smart trainer. Ride is Primary, so a test is due, but there's no outdoor test.
  - **Two of the three Strength Add-ons** (`addon-upper`, `addon-posterior`) need a kettlebell, which isn't in `equipment` (the gym has none). Only `addon-core` (bands, bodyweight) can be planned, so every Add-on is `addon-core` until the Bank has more.
