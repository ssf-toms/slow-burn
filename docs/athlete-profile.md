# Athlete Profile

The lasting description of the person being planned for (see `GLOSSARY.md`). Setup writes it and the Check-in and Adjustment skills read it. It lives at `athlete/profile.md` in the private `athlete/` repo, next to `athlete/weeks/`. `examples/profile.md`, `examples/profile-home.md` and `examples/profile-gym.md` (two Places) show three complete, invented profiles.

The frontmatter holds the structured fields. The body holds the approved Week Templates and free notes. The templates are generated from the fields at Setup and only change when Setup is run again (ADR 0003). The rules for generating them are in `docs/planning-rules.md`.

## Format

```markdown
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

## Week Templates

| Day | Light | Normal | Push |
|-----|-------|--------|------|
| Mon | Recovery: rest | Recovery: rest | Recovery: rest |
| …   | …     | …      | …    |

## Notes

Free text: goals, injuries, preferences, and the gaps Setup found.
```

The frontmatter is a small subset of YAML, so the stdlib-only client can read it without a YAML library:
- top-level `key: value` lines;
- one level of nesting, indented two spaces (`tiers`, `places`, `availability`, `setup`), and a second level only under `availability.fixed`;
- lists written inline as `[a, b]` (each Place's Equipment), or as `- {…}` lines for `other`;
- strings that hold a colon or a dash, such as the pace, in double quotes.

Leave a conditional field out when it doesn't apply. Don't write it as empty.

## Fields

Setup asks the questions in this order. "Asked" says when Setup asks for a field. A field that isn't asked isn't written.

| Field | Shape | Asked | Notes |
|-------|-------|-------|-------|
| `tiers` | map of activity → `primary` \| `secondary` \| `occasional` | Always | The activities are `ride`, `run`, `swim`, `walk`, `strength` and `pt`. Leave an activity out if it isn't planned at all. At least one activity is needed. |
| `other` | list of `{id, name, minutes, counts_as}` | Always: "anything else you do regularly?" Write `[]` for none | Free-form activities, delivered as calendar notes. `counts_as` is `training` (an `Other` Session) or `recovery` (it can fill a Recovery Day). Never Quality, never paired, and no Equipment. The `id` is lowercase with dashes. In the Week Record it's written `other:<id>`. |
| `places` | map of Place → list of Equipment tags | Always: "where do you train?", then the Equipment at each Place. Most athletes have one Place, written `home` | The first Place is the default: a day is there unless its template cell or Plan row says `@<place>`. The tags are `bodyweight`, `bands`, `band-anchor` (a door anchor or post to pull a band against), `kettlebell`, `dumbbells`, `barbell` (with a rack), `bench`, `cable` (a cable station), `pull-up-bar`, `smart-trainer`, `pool` and `hr-strap`. There's no `gym` tag: a gym is a Place, and its Equipment is listed item by item. A Workout or Exercise can only be planned on a day if every tag it needs is at that day's Place, with one exception: on a ride pushed as a structured workout (`delivery: workout`), `smart-trainer` only decides whether it's pushed as indoor or outdoor (indoor only if the day's Place has one), so the ride can be planned without one. The FTP test is a note, so it still needs a smart trainer. An Alternative is a swap on the day, so it may need the Equipment of any one Place. |
| `experience` | `new` \| `some` \| `experienced` | Only if ride or run is Primary (the sports with Ladders) | Sets the starting Ladder step: 1, 2 or 3, for each Primary sport that has Ladders. |
| `availability.days_per_week` | number, 3–6 | Always | The number of training days in a Push week. Normal has one fewer, Light two fewer. The rest are Recovery Days, so at most 6 (Push keeps one) and at least 3 (Light keeps one training day). |
| `availability.fixed` | map of day → value | Always: "any day that's always the same?" Write `{}` for none | Days placed first when generating. The value is `rest` (a Recovery Day with no Workout), `recovery` (any Recovery Day), a tiered activity (`strength`, `swim`, …) or `other:<id>`, ending in ` @<place>` if the day isn't at the default Place: a weekly gym session is `Tue: strength @gym`. |
| `easy_run_pace` | string, e.g. `"5:45–6:00/km"` | Only if `run` is tiered | Put into run Workouts in place of `{easy_run_pace}` when they're pushed. |
| `threshold_run_pace` | string, e.g. `"4:50/km"` | Only if `run` is Primary | The pace you could race for about an hour. Run Quality Workouts write their targets as `{threshold_run_pace}` plus an offset ("+15–20 s/km"), filled in when they're pushed. Updated after each run test (`run-test-20`). If unknown, the first run Quality slot is the run test. |
| `pairings` | list, e.g. `[pt+strength]` | Only if two or more of `pt`, `strength` and `walk` are tiered. Write `[]` if asked and there are none | Workouts that may share one Session, joined by `+`. Nothing is ever paired with a Quality Session, and `other` activities are never paired. |
| `alternatives` | `on` \| `off` | Only if two or more of `ride`, `run` and `swim` are tiered. Left out means `off` | Whether every Endurance Session names an Alternative in another sport. |
| `ftp` | number (watts) | Only if `ride` is tiered | Moved out of `.env`. Updated after each FTP test. |
| `lthr`, `max_hr` | numbers (bpm) | Only if `ride` is tiered | Lactate-threshold and maximum heart rate, for intervals.icu zones. |
| `setup` | map | Never: Setup writes it | The intervals.icu steps that are already done, so a re-run can skip them: `sync_verified` (a test ride reached the trainer app) and `strava_connected`, each `yes` or `no`. Replaces `SYNC_VERIFIED` and `STRAVA_CONNECTED` in `.env`. |

## Week Templates

The body has a `## Week Templates` section with one table. It has the same columns as the old fixed tables in `docs/planning-rules.md`: `Day`, then one column per Week Level, in the order `Light`, `Normal`, `Push`. There's one row for each day, Mon to Sun.

Each cell is a Session kind, a colon, and what fills it:

| Kind | What follows | Example |
|------|--------------|---------|
| `Recovery` | `pt`, `walk`, `rest`, or a recovery-type `other:<id>` | `Recovery: pt` |
| `Quality` | the Primary sport with Ladders that gets the slot | `Quality: ride` |
| `Endurance` | `ride`, `run` or `swim` | `Endurance: run` |
| `Strength` | `strength`, alone or in an allowed pairing | `Strength: pt, strength` |
| `Other` | a training-type `other:<id>` | `Other: other:pilates` |

Optional parts, in this order:
- **Pairing:** activities separated by commas, in the order done (`pt, strength`). The pair must be in `pairings`.
- **Choice:** ` or ` between options, picked at the Check-in (`Recovery: pt or walk`).
- **Alternative:** ` (alt: <activity>)` after an Endurance Session names the sport to offer as the Alternative. Only if `alternatives: on`. Without it, the Check-in picks the Alternative.
- **Add-on:** ` + Add-on` at the end of an Endurance cell, only if `strength` is tiered.
- **Place:** ` @<place>` at the very end, if the day isn't at the default Place (`Strength: strength @gym`, `Endurance: swim @gym`). It names a Place in `places` and applies to the whole cell.

The template doesn't name Workouts or Ladders. The Check-in picks them with the rules in `bank/README.md`, and the Level picks each Workout's Dose. The FTP test isn't in the template either: when it's due, it replaces a Quality slot.

## Notes

Anything else, in free text, under `## Notes`: goals, injuries, preferences, and the **gaps** Setup found, such as a tiered sport with no Workouts in the Bank, or Workouts that need Equipment the athlete doesn't have. Gaps are listed, never filled with invented Workouts.
