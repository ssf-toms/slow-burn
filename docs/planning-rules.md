# Planning rules

The rules for shaping a Week Plan, shared by Setup and the Check-in and Adjustment skills. Terms follow `GLOSSARY.md`. The rules for choosing which Workout goes in each slot (Ladders, rotation, FTP test) live in `bank/README.md`. The Athlete Profile format, including the template cell syntax, is in `docs/athlete-profile.md`.

## Generating Week Templates

Every Week Plan starts from the Week Template for its Week Level. The templates aren't fixed: Setup generates Light, Normal and Push from the Athlete Profile, the athlete approves them, and they're stored in the profile (ADR 0003). The Check-in fills the stored template and doesn't regenerate it.

Apply these rules in order:

1. **Training days:** Push has `availability.days_per_week` training days, Normal one fewer, Light two fewer. Every other day is a Recovery Day: PT, a walk, rest, or a recovery-type `other` activity. There's always at least one Recovery Day.
2. **Quality slots:** Normal and Push get two Quality Sessions, Light at most one. They go only to Primary sports that have Ladders (today, only `ride`). With one such sport, it gets both slots. With two, one each. With three, the slots rotate week to week. With none, there are no Quality Sessions and the training days are Endurance, Strength or `Other`.
3. **Tier counts:** each Primary activity is on at least 2 training days a week, each Secondary on 1–2, and each Occasional on at most 1, or only as an Alternative. A Strength Add-on counts as a strength day. For the Recovery activities (PT and walk), a Primary or Secondary Tier is met on Recovery Days as well as training days: PT on a Recovery Day counts toward its 2 or 1–2 days. If the training days can't hold every Primary at 2 and every Secondary at 1 (as in a short Light week), the Primaries keep their days and a Secondary that doesn't fit becomes a named Alternative. Judgement fills the remaining days, and the athlete approves the result.
4. **Spacing:** Quality Sessions are never on consecutive days. Strength has no spacing rules of its own.
5. **Fixed days:** the days in `availability.fixed` are placed first, before any other rule fills the week.
6. **Dose:** the template sets the Session kind, and the Level sets each Workout's Dose. The Endurance ride length (50′ in Light, 60′ in Normal, 60′ plus one 75′ in Push) is the first case of this.
7. **Conditional parts:**
   - The FTP test is planned only if ride is Primary.
   - Load Warning rules 3 and 4 apply only if ride is Primary or Secondary (not Occasional). Otherwise use rules 1 and 2 plus judgement.
   - Setup asks for FTP and heart rate only if ride is tiered.
   - The MyWhoosh steps apply only if `equipment` includes `smart-trainer`.

The same rules hold for every template:
- **One Session a day.** A Strength Add-on is the only thing that can follow it, and only after an Endurance Session or a Test Session's easy spin. It needs `strength` tiered.
- **Pairings:** a Session combines Workouts (such as PT then strength) only if the pair is in `pairings`. Nothing is ever paired with a Quality Session.
- **Alternatives:** if `alternatives: on`, every Endurance Session names an Alternative in another tiered sport, so you can swap on the day.
- **Equipment:** a Workout can be planned only if every tag it needs is in `equipment` (the one exception, `smart-trainer` on a structured ride, is in `docs/athlete-profile.md`). A slot the Bank can't fill is listed as a gap in the profile's Notes, never filled with an invented Workout.
- **Real life wins.** If the user names a one-off constraint (a busy day, travel), move Sessions around it within the Adjustment rules below rather than forcing the template. A lasting change means re-running Setup.

### Worked example

The maintainer's profile: ride and PT Primary, strength Secondary, run and walk Occasional, `days_per_week: 6`, `fixed: {Mon: strength}`, `pairings: [pt+strength]`, `alternatives: on`, and a smart trainer.

| Day | Light | Normal | Push |
|-----|-------|--------|------|
| Mon | Strength: pt, strength | Strength: pt, strength | Strength: pt, strength |
| Tue | Quality: ride | Quality: ride | Quality: ride |
| Wed | Endurance: ride (alt: run) + Add-on | Endurance: ride (alt: run) + Add-on | Endurance: ride (alt: run) + Add-on |
| Thu | Recovery: pt | Quality: ride | Quality: ride |
| Fri | Recovery: walk | Recovery: pt | Endurance: ride (alt: run) |
| Sat | Endurance: ride (alt: run) | Endurance: ride (alt: run) | Endurance: ride (alt: run) |
| Sun | Recovery: pt | Recovery: pt or walk | Recovery: pt or walk |

How the rules were applied:
- **Fixed days:** Monday's PT and strength is placed first. It's a Strength Session, so Monday is now a training day, where the old fixed tables called it a Recovery Day.
- **Training days:** 4 (Light), 5 (Normal) and 6 (Push), so Push keeps Sunday as a Recovery Day. Compared with the old tables, Monday's new training day costs one Endurance Session at each Level (Light's Tuesday and Friday, Normal's Sunday, Push's Sunday).
- **Quality:** ride is the only Primary sport with Ladders, so it gets both slots, Tuesday and Thursday as before. Light keeps one, on Tuesday (an easy Sweet Spot, see rule 1 in `bank/README.md`).
- **Tiers:** ride is on at least 2 days at every Level. PT is on Monday and at least one Recovery Day. Strength is Monday plus Wednesday's Add-on. Run is an Alternative only, and the walk is on at most one day.
- **Dose:** Light rides are 50′, Normal 60′, and Push's Saturday ride is the long one (75′).

## Load Warnings

Evaluate the rules at every Check-in, and report each one as triggered, clear or not applicable:

1. **2 Push weeks:** the last two Week Records were both `push`.
2. **3 Normal+ weeks:** the last three Week Records were all `normal` or `push`.
3. **Form ≤ −20:** intervals.icu form (fitness minus fatigue) on the latest day.
4. **Ramp > 6:** the intervals.icu ramp rate on the latest day.

- **If any rule triggers,** recommend Light and say which rule triggered. It's advice only: the user decides, and the outcome goes in `load_warning` as `"<rule>; accepted"` or `"<rule>; overridden"`.
- **Rules 3 and 4 apply only if ride is Primary or Secondary** (not Occasional, generation rule 7). Otherwise report them as not applicable and use rules 1 and 2 plus judgement about the reported Sessions.
- **Rules 3 and 4 count rides only** (ADR 0002). Weigh the runs and other Sessions the user reports by judgement, and mention that you did.
- **Rules 3 and 4 need at least 6 weeks of ride history.** Until then, report them as "not enough data yet" and rely on rules 1 and 2.

## Adjustment rules

When a Week Plan changes mid-week:

- **Quality Sessions:** keep them on non-consecutive days, with at least one non-Quality day between.
- **A missed Quality Session** is dropped. It moves only into a day that keeps the spacing above and replaces an Endurance Session.
- **Endurance Sessions** swap freely: to their Alternative (if `alternatives: on`), or between days.
- **Recovery Days** stay in the week. They are PT, a walk, rest, or a recovery-type `other` activity. When a day is lost, an Endurance Session gives way first.
- **One Session a day** still holds.
- **No Workout to fill a Session:** if a moved or swapped Session has no Workout the profile can fill (missing Equipment, or a gap in the Bank such as no swim Workouts), flag it to the user. Never invent a Workout.
- **Illness:** each sick day becomes a Recovery row with an empty Workout (rest). The first day back is Endurance or a walk, never Quality. If symptoms are above the neck only (a cold) and mild, a walk is fine.
