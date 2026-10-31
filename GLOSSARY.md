# Slow Burn

A personal system for planning a week of training ahead of time: cycling, running, swimming, strength and mobility, aimed at aerobic fitness and durability rather than competition.

## Language

### Athlete

**Athlete Profile**:
The lasting description of the person being planned for: their Sport Tiers, Equipment, experience, availability, easy and threshold run pace, Places, and their FTP and heart-rate numbers. Their Week Templates are generated from it.
_Avoid_: Settings, config, user

**Sport Tier**:
How much an activity counts in the Athlete Profile. Every activity has a Tier, including strength and mobility, so a profile can be just mobility and home strength. **Primary** activities get the most Sessions, and a Quality slot each where they have Ladders. **Secondary** activities get one or two steady, easy Sessions a week. **Occasional** activities appear as an Alternative or a single Session. More than one activity can be Primary.
_Avoid_: Weight, priority, percentage

**Tiered**:
Said of an activity that has a Sport Tier in the Athlete Profile, at any Tier, Occasional included. An activity that isn't tiered is never planned. "Ride is tiered" and "ride is Primary" are different conditions.
_Avoid_: Enabled, active, selected

**Equipment**:
What the athlete has access to for training at a Place, as a list (for example bodyweight, bands, kettlebell, dumbbells, barbell, smart trainer, pool). A Workout or Exercise can be planned on a day only if that day's Place has all the Equipment it needs, except that a structured ride doesn't need the smart trainer: it only decides whether the ride is indoor or outdoor.
_Avoid_: Gear, kit

**Place**:
A named spot where the athlete trains (home, gym), with its own Equipment, listed in the Athlete Profile. A Week Template says which Place each day's Session is at. Most athletes have one Place.
_Avoid_: Location, venue, site

**Setup**:
The one-time conversation that builds the Athlete Profile, approves the Week Templates, and connects intervals.icu. It can be run again to change the profile.
_Avoid_: Onboarding, wizard, install

### Workouts

**Workout**:
A reusable definition of a training activity (structure, targets, instructions) kept in the Workout Bank. A Session is a Workout placed on a day.
_Avoid_: Session (when meaning the definition), template, routine

**Dose**:
How much of a Workout is done at a given Week Level: rounds or Exercises for strength and mobility, minutes for an Endurance ride or run. The Workout states its Dose for each Level.
_Avoid_: Volume, size, amount

**Extension**:
10–15 extra minutes at Endurance added before the cooldown of one Quality ride in a Push week, now and then. It's written `+<minutes>` after the Workout's ID in the Week Plan (`th-2 +15`). It's part of the Dose, so the Workout itself doesn't change.
_Avoid_: Bonus, extra volume

**Exercise**:
A single strength or mobility movement (a goblet squat, a band row, a hip flexor stretch) with its movement pattern and the Equipment it needs, kept in the Workout Bank. Strength Sessions, Strength Add-ons and Mobility Sessions are composed from Exercises; across a week, strength covers every pattern.
_Avoid_: Move, drill, lift

**Workout Bank**:
Everything a Week Plan draws from: the Core Bank plus the athlete's Personal Workouts and Personal Exercises.
_Avoid_: Library, catalogue, database

**Core Bank**:
The curated part of the Workout Bank that ships with Slow Burn: foundational, widely applicable Workouts and Exercises chosen for function and variety, not completeness.
_Avoid_: Default bank, built-ins

**Personal Workout**:
A Workout the athlete adds themselves, kept in their own repo, which counts as part of their Workout Bank once it passes the Bank's checklist of principles. Personal Workouts and Personal Exercises together are the Personal part of the Workout Bank.
_Avoid_: Custom workout, user workout

**Personal Exercise**:
An Exercise the athlete adds themselves (a machine at their gym, a move from their physio), kept in their own repo. Like a Personal Workout, it counts as part of their Workout Bank once it passes the Bank's checklist of principles, and it's composed into Sessions like any Core Exercise.
_Avoid_: Custom exercise, user exercise

**Bank gap**:
A slot an athlete's Week Templates call for that the Workout Bank can't fill for them: a tiered sport with no Workouts, or Workouts that all need Equipment the athlete lacks. Setup lists gaps in the Athlete Profile's Notes. A gap can be closed by a Personal Workout or Personal Exercise that passes the checklist, never by an unchecked one made up on the spot. Called a gap for short.
_Avoid_: Missing workout, hole, TODO

**Ladder**:
An ordered sequence of Workouts of one Quality type in one sport, each slightly harder than the last. You move up a step after completing the current one at an effort of 7/10 or below.
_Avoid_: Progression, plan, series

### Days and sessions

**Session**:
The main planned activity for a day. A day has exactly one Session, optionally followed by a Strength Add-on. A Session can combine Workouts (such as mobility then strength) only if the athlete chose that pairing in their Athlete Profile.
_Avoid_: Workout (when meaning the scheduled thing), activity, training

**Pairing**:
Two Workouts the athlete has chosen to combine in one Session (such as mobility then strength), listed in the Athlete Profile. Nothing is paired with a Quality Session, and Other activities are never paired.
_Avoid_: Combo, superset, double

**Quality Session**:
A ride or run with deliberate time above endurance intensity (tempo, sweet spot, threshold, VO2max).
_Avoid_: Hard workout, intervals day, key session

**Endurance Session**:
A ride or run held at easy, Zone 2 intensity.
_Avoid_: Base ride, easy ride, Z2

**Alternative**:
A Workout of similar effort in another sport, named next to an Endurance Session so it can be swapped in on the day. Whether Alternatives are offered is the athlete's choice.
_Avoid_: Backup, substitute, option

**Strength Session**:
A resistance session (bodyweight, bands, weights) that stands as a day's Session, composed fresh for each Week Plan from the Exercises its day's Place allows. It is a training day, never a Recovery Day.
_Avoid_: Gym, lifting, conditioning

**Strength Add-on**:
A short (~15 min) block of Exercises done straight after an Endurance Session or a Test Session's easy spin; it never follows a Quality Session.
_Avoid_: Finisher, extra

**Test Session**:
A day built around a fitness test that resets a Primary sport's targets: the FTP test followed by an easy spin for ride, or a time trial that sets threshold pace for run.
_Avoid_: Test day, benchmark

**Mobility Session**:
A ~30 min session of mobility work, done for maintenance: a whole mobility Workout (such as a physical-therapy routine the athlete keeps as a Personal Workout), a session composed from mobility Exercises, or a routine with a few Exercises added. It's one activity, so this isn't a Pairing.
_Avoid_: PT Session, rehab, stretching

**Other**:
A free-form activity the athlete does regularly outside the Workout Bank (a Pilates class, say), listed in the Athlete Profile's `other` and written `other:<id>` in a Week Plan. It counts either as training, as an `Other` Session on a training day, or as recovery, filling a Recovery Day. It's pushed as a calendar note, never Quality and never paired. Unlike a Personal Workout, its content isn't the athlete's to define (a class, a club run), so it has no Dose and skips the Bank's checklist.
_Avoid_: Custom workout, misc, extra

**Recovery Day**:
A day whose Session is a Mobility Session, a walk, a recovery-type Other activity, or full rest. Every other day is a training day.
_Avoid_: Rest day, off day

### Planning

**Week Plan**:
The seven Sessions chosen for one upcoming week, decided before the week starts.
_Avoid_: Schedule, program, block

**Week Template**:
The Mon–Sun pattern of Session kinds that every Week Plan starts from. There is one for each Week Level, generated from the Athlete Profile and approved at Setup.
_Avoid_: Default week, pattern

**Week Level**:
How hard a Week Plan is meant to be, chosen at the Check-in. A Level sets two things: how many of the athlete's available days are training days, and the Dose of each Workout. **Push** uses every available day, **Normal** one fewer, **Light** two fewer, and the remaining days are Recovery Days, always at least one. Light has at most one Quality Session.
_Avoid_: Intensity, difficulty, load

**Check-in**:
The weekly conversation in which last week is reviewed and the next Week Plan, with its Week Level, is agreed.
_Avoid_: Planning session, review

**Adjustment**:
A mid-week reshuffle of the remaining Sessions of the current Week Plan when life intervenes.
_Avoid_: Reschedule, replan

**Week Record**:
The lasting account of one week: its Week Plan, the Week Level and the reasoning behind it, Adjustments, and what was actually done and reported.
_Avoid_: Log, journal, history

**Load Warning**:
An advisory raised at a Check-in suggesting a Light week. It is raised after recent hard weeks or when ride-based fitness/fatigue numbers look stretched. It never overrides your choice.
_Avoid_: Alert, block, overtraining flag
