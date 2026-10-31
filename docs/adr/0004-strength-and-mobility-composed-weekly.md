# Strength and mobility are composed from Exercises each week, not fixed Workouts

Strength Sessions, Strength Add-ons and Mobility Sessions are composed fresh at every Check-in from the Exercises the day's Place allows, rather than drawn from fixed Workouts such as the old `str-a/b/c` cycle. Equipment varies too much between athletes (and between Places for one athlete) for a handful of fixed sessions to fit everyone, and the foundational movements number in the dozens, so a fixed A/B/C cycle limits exposure. Balance is kept across the week, not per Session: all strength in the week together covers every movement pattern, and a lone Strength Session is full-body. We considered composing once at Setup and keeping the result fixed (like Week Templates, ADR 0003), which makes progression easy to follow, and chose variety instead.

## Consequences

- Progression isn't tracked per Exercise. The Level sets the Dose, each Exercise carries a Progress line, and problems are raised by the athlete at the Check-in's look-back.
- A composed Session has no Workout ID, so the Week Plan row lists its Exercise IDs; that's what is pushed, kept in the Week Record, and used to vary next week's picks.
- The old strength and Add-on Workouts are retired and their moves become Exercises; Week Records that name the old IDs stay as they are.
