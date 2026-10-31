# Local folder owns the Workout Bank and Week Records; intervals.icu is delivery only

The Workout Bank and every Week Record live as Markdown files in this folder, which is the source of truth. intervals.icu (free) is used only to deliver planned Sessions and to supply completed-ride data. Planned rides it holds sync automatically into the MyWhoosh calendar 7 days ahead, and its iCal feed puts every Session into your calendar app. We chose this over MyWhoosh's built-in plans and calendar because its 770+ library workouts have no stable IDs, can't be reasoned about, and offer no load tracking or automation. We chose it over keeping the Bank in an intervals.icu library because the local skills need to read, version and reason over Workouts (including strength and PT, which intervals.icu can't describe well).

## Consequences

- Workouts pushed to MyWhoosh must use %FTP targets and simple step/repeat structure. Ramps degrade to flat averages and cadence targets are dropped.
- Anything edited directly in intervals.icu is overwritten by the next push from the local files.
