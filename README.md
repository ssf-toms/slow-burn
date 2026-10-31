# Slow Burn

A weekly training planner for aerobic fitness and durability, not racing. It plans your mix of cycling (indoors or out), running, strength and physical therapy around the Equipment you have. Each week you have a short conversation with [Claude Code](https://claude.com/claude-code): it reviews the week just gone, agrees the next one with you, and pushes it to [intervals.icu](https://intervals.icu). From there, rides can sync to a trainer app such as MyWhoosh, and every Session shows up in your calendar.

## The idea

- **Start from you.** A one-time **Setup** builds your **Athlete Profile**: a **Sport Tier** for each activity (Primary, Secondary, Occasional), the **Equipment** you have, your experience and the days you can train. It generates your **Week Templates** from that, and only plans Workouts your Equipment allows. Where the Bank has nothing to fill a slot (there are no swim Ladders yet, for example), Setup tells you instead of inventing one, and can help you add your own **Personal Workout** or Exercise, checked against the Bank's principles (`/add-workout`).
- **Plan the week before it starts.** A Sunday **Check-in** reviews the week and picks a **Week Level**: Light, Normal or Push. A Level picks how many of your available days are training days, and the Dose of each Workout (rounds for strength and PT, minutes for an Endurance ride).
- **Climb slowly.** Quality rides and runs sit on **Ladders** (Sweet Spot or run Tempo, Threshold, VO2max). You move up a step only after finishing the current one at an effort of 7/10 or below.
- **Back off before you need to.** **Load Warnings** suggest a Light week after a run of hard weeks, or when fitness and fatigue numbers look stretched. They're advice only: you decide.
- **Real life wins.** An **Adjustment** reshuffles the rest of the week when you're ill, short of time or travelling, or the weather is good, without breaking the spacing rules.

The vocabulary is defined in [`GLOSSARY.md`](GLOSSARY.md), the rules in [`docs/planning-rules.md`](docs/planning-rules.md) and [`bank/README.md`](bank/README.md), and the design decisions in [`docs/adr/`](docs/adr/).

## What's here

| Path | What it is |
|------|------------|
| `bank/` | The **Workout Bank**: one Markdown file per Workout. Ride files hold intervals.icu workout text in %FTP |
| `docs/` | Planning rules, the Athlete Profile and Week Record formats, ADRs |
| `.claude/skills/` | The `/setup` skill that builds your profile and connects intervals.icu, the `/checkin` and `/adjust` skills that run the weekly conversation, and `/add-workout`, which adds a Personal Workout or Exercise |
| `scripts/icu.py` | intervals.icu client: push a week, list events, rides and fitness |
| `examples/` | Invented Athlete Profiles and Week Records |
| `athlete/` | **Yours**: your Athlete Profile, Week Records (`athlete/weeks/`) and Personal Workouts and Exercises (`athlete/bank/`). Ignored by this repo; `/setup` makes it its own private git repo |

## Setup

Requirements: macOS, Python 3, Claude Code, and a free intervals.icu account (Setup helps you make one). macOS is needed because the intervals.icu API key is kept in the Keychain; that is the one remaining macOS dependency.

1. Clone this repo.
2. Open Claude Code in the repo and run `/setup`. It asks about your sports, Equipment and week, shows you the Week Templates it generates, then walks you through intervals.icu, the calendar feed and a test ride. You store the API key in the Keychain yourself; it never goes in the chat.
3. Push `athlete/` to a **private** remote if you want a backup.
4. Run `/checkin` to plan your first week.

Run `/setup` again whenever your sports, Equipment or availability change.

## Each week

- **Sunday (or Monday morning):** `/checkin`. Review last week, choose a Level, approve the Week Plan, and it's pushed and committed to `athlete/weeks/`.
- **Mid-week, if needed:** `/adjust`. Reshuffle the rest of the week and re-push it.
- **Whenever you want something the Bank lacks:** `/add-workout`. Describe it or paste your own routine; it's checked against the Bank's principles and saved to `athlete/bank/`.

Runs, swims, PT and walks aren't synced: you report them at the Check-in ([ADR 0002](docs/adr/0002-runs-reported-not-synced.md)).

## License

[MIT](LICENSE)
