# Week Templates are generated once from the Athlete Profile, not rebuilt each Check-in

Each athlete's Light, Normal and Push Week Templates are generated from their Athlete Profile (Sport Tiers, Equipment, availability, pairings) during Setup. The athlete approves them and they're stored in the profile. They're only regenerated when the profile changes. Every Check-in fills the stored template, the way it used the fixed tables before. The alternative was to rebuild the week from the Tiers at every Check-in. That gives more variety, but weeks become unpredictable from one to the next, and the spacing and Level rules are harder to check. A template that's stored and approved keeps the weekly routine stable and turns the Check-in into "fill the slots", not "design a week".

## Consequences

- The fixed Mon–Sun tables in `docs/planning-rules.md` are replaced by rules for generating templates. The maintainer's own profile produces something close to the old tables, but not necessarily identical.
- A change to the profile (new sport, new Equipment, different availability) only takes effect after Setup is re-run and the new templates are approved.
