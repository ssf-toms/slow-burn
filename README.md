# Slow Burn

A weekly training planner for aerobic fitness and durability, not racing. It covers indoor and outdoor cycling, easy running, kettlebell and band strength, and physical therapy. Each week you have a short conversation with [Claude Code](https://claude.com/claude-code): it reviews the week just gone, agrees the next one with you, and pushes it to [intervals.icu](https://intervals.icu). From there, rides sync to MyWhoosh and every Session shows up in your calendar.

## The idea

- **Plan the week before it starts.** A Sunday **Check-in** reviews the week and picks a **Week Level**: Light, Normal or Push. Levels change how many cardio days the week has, not how long the Sessions are.
- **Climb slowly.** Quality rides sit on **Ladders** (Sweet Spot, Threshold, VO2max). You move up a step only after finishing the current one at an effort of 7/10 or below.
- **Back off before you need to.** **Load Warnings** suggest a Light week after a run of hard weeks, or when fitness and fatigue numbers look stretched. They're advice only: you decide.
- **Real life wins.** An **Adjustment** reshuffles the rest of the week when you're ill, short of time or travelling, or the weather is good, without breaking the spacing rules.

The vocabulary is defined in [`GLOSSARY.md`](GLOSSARY.md), the rules in [`docs/planning-rules.md`](docs/planning-rules.md) and [`bank/README.md`](bank/README.md), and the design decisions in [`docs/adr/`](docs/adr/).

## What's here

| Path | What it is |
|------|------------|
| `bank/` | The **Workout Bank**: one Markdown file per Workout. Ride files hold intervals.icu workout text in %FTP |
| `docs/` | Planning rules, the Week Record format, ADRs |
| `.claude/skills/` | The `/checkin` and `/adjust` skills that run the weekly conversation |
| `scripts/icu.py` | intervals.icu client: push a week, list events, rides and fitness |
| `scripts/setup-intervals.sh` | Interactive setup for intervals.icu, MyWhoosh and Apple Calendar |
| `examples/` | An invented, completed Week Record |
| `weeks/` | **Your** Week Records. Ignored by this repo; make it its own private repo |

## Setup

Requirements: macOS (the API key is kept in the Keychain), Python 3, `jq`, Claude Code, and a free intervals.icu account.

1. Clone this repo.
2. Run `./scripts/setup-intervals.sh`. It walks you through FTP and heart rate, connecting MyWhoosh, storing your API key, the calendar feed and a test ride. It writes `.env` (see `.env.example`).
3. Make your log: `mkdir weeks && git init weeks`. Push it to a **private** remote if you want a backup.
4. Make the Bank yours. The paces in the run files, the strength and PT contents, and the Workouts themselves are a starting point.
5. Open Claude Code in the repo and run `/checkin`.

## Each week

- **Sunday (or Monday morning):** `/checkin`. Review last week, choose a Level, approve the Week Plan, and it's pushed and committed to `weeks/`.
- **Mid-week, if needed:** `/adjust`. Reshuffle the rest of the week and re-push it.

Runs, PT and walks aren't synced: you report them at the Check-in ([ADR 0002](docs/adr/0002-runs-reported-not-synced.md)).

## License

[MIT](LICENSE)
