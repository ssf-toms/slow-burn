# Planning rules

The rules for shaping a Week Plan, shared by the Check-in and Adjustment skills. Terms follow `GLOSSARY.md`. The rules for choosing which Workout goes in each slot (Ladders, rotation, FTP test) live in `bank/README.md`.

## Week Templates

Every Week Plan starts from the template for its Week Level.

| Day | Light (~3.3 h) | Normal (~5 h) | Push (~6 h) |
|-----|----------------|---------------|-------------|
| Mon | Recovery: pt, strength | Recovery: pt, strength | Recovery: pt, strength |
| Tue | Endurance, or an easy Sweet Spot¹ | Quality | Quality |
| Wed | Endurance + Add-on | Endurance + Add-on | Endurance + Add-on |
| Thu | Recovery: pt | Quality | Quality |
| Fri | Endurance | Recovery: pt | Endurance |
| Sat | Endurance | Endurance | Endurance (75′) |
| Sun | Recovery: pt or rec-walk | Endurance | Endurance |

¹ See rule 1 in `bank/README.md`.

- **One Session a day.** An Add-on is the only extra, and only after an Endurance Session or on a Test day (after the easy spin).
- **Quality Sessions are rides.** Every Endurance Session is a ride with a run alternative, so you can swap on the day.
- **Recovery Days stay off the bike:** PT, strength, or a walk.
- **Real life wins.** If the user names a fixed constraint (a busy day, travel), move Sessions around it within the Adjustment rules below rather than forcing the template.

## Load Warnings

Evaluate all four rules at every Check-in, and report each one as triggered or clear:

1. **2 Push weeks:** the last two Week Records were both `push`.
2. **3 Normal+ weeks:** the last three Week Records were all `normal` or `push`.
3. **Form ≤ −20:** intervals.icu form (fitness minus fatigue) on the latest day.
4. **Ramp > 6:** the intervals.icu ramp rate on the latest day.

- **If any rule triggers,** recommend Light and say which rule triggered. It's advice only: the user decides, and the outcome goes in `load_warning` as `"<rule>; accepted"` or `"<rule>; overridden"`.
- **Rules 3 and 4 count rides only** (ADR 0002). Weigh the runs the user reports by judgement, and mention that you did.
- **Rules 3 and 4 need at least 6 weeks of ride history.** Until then, report them as "not enough data yet" and rely on rules 1 and 2.

## Adjustment rules

When a Week Plan changes mid-week:

- **Quality Sessions:** keep them on non-consecutive days, with at least one non-Quality day between.
- **A missed Quality Session** is dropped. It moves only into a day that keeps the spacing above and replaces an Endurance Session.
- **Endurance Sessions** swap freely: ride ↔ run alternative, or between days.
- **Recovery Days** stay in the week. When a day is lost, an Endurance Session gives way first.
- **One Session a day** still holds.
- **Illness:** each sick day becomes a Recovery row with an empty Workout (rest). The first day back is Endurance or `rec-walk`, never Quality. If symptoms are above the neck only (a cold) and mild, a walk is fine.
