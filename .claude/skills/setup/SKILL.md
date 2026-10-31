---
name: setup
description: Setup. Build or change the Athlete Profile, generate and approve the Week Templates, and connect intervals.icu. Use when the user wants to set up Slow Burn, change their profile (sports, Equipment, availability), or reconnect intervals.icu, or when the Check-in finds no profile.
---

# Setup

Speak in the terms from `GLOSSARY.md`. Read these before step 1:

- `docs/athlete-profile.md`: the profile format, which fields to ask and when, and the template cell syntax
- `docs/planning-rules.md`: the rules for generating Week Templates
- `bank/README.md`: the Workout frontmatter, the Personal part and the Index

`examples/profile.md`, `examples/profile-home.md` and `examples/profile-gym.md` (home plus a weekly gym day) are three finished profiles to model yours on.

Ask the user's decisions with the AskUserQuestion tool, recommended option first.

The client is `scripts/icu.py`. Run it from the repo root. Open web pages for the user with `open <url>`.

The intervals.icu API key stays with the user. They store it in the Keychain themselves with the command in step 5. Never ask for it, and if they paste one into the chat, tell them to revoke it in intervals.icu and make a new one.

## 1. Detect

1. **Profile exists** (`athlete/profile.md`): show a short summary (Tiers, Places and their Equipment, days per week, fixed days, the `setup` block). Ask what to change and jump to it:
   - any profile field: step 2 for those fields only, then steps 3 and 4;
   - the templates only: step 4;
   - intervals.icu, the calendar or the test ride: step 5, 6 or 7.
2. **No profile:** create `athlete/` and run `git init athlete`.

**Done when** `athlete/` is a git repo and you know which steps to run.

## 2. Profile

Ask in the order of the Fields table in `docs/athlete-profile.md`, and skip each field whose "Asked" condition doesn't hold. A field that isn't asked isn't written.

1. **Tiers:** which of ride, run, swim, walk, strength and PT they plan, then the tier of each (Primary, Secondary, Occasional). Then "anything else you do regularly?" for `other`: name, minutes, and whether it counts as training or recovery.
2. **Places:** "where do you train?" Default to one Place, `home`. List the main one first: it's the default. Then the Equipment tags at each Place. A gym is a Place, not a tag, so ask what it has item by item (`barbell`, `bench`, `cable`, `pull-up-bar`, `machines`, `dumbbells`, …). With `bands`, ask whether they have a door anchor or post to pull against (`band-anchor`).
3. **Experience,** then **availability:** `days_per_week`, then fixed days, each with its ` @<place>` if it isn't at the default Place (`Wed: strength @gym`).
4. **Easy run pace,** then **threshold run pace** (if run is Primary: the pace they could race for about an hour, or their 10 km race pace; if they don't know, leave it out, note it, and make the first run Quality slot the run test), then **pairings** and **Alternatives.**
5. **FTP, LTHR and max HR,** if ride is tiered. If they have an intervals.icu account, open `https://intervals.icu/settings`: FTP is under Ride → Power level settings, LTHR and max HR under Ride → HR Zone settings. They read the values there, or enter them there if they're new. With no account yet, ask for the numbers now and enter them in intervals.icu in step 5. Leave out any value they don't know, and note it in the profile's Notes.

**Done when** every field whose condition holds has a value or a note saying it's unknown.

## 3. Bank gaps

1. Run `grep -rH '^sport:\|^kind:\|^ladder:\|^equipment:\|^delivery:' bank athlete/bank --include='*.md'`. Files under `athlete/bank/` are the athlete's Personal Workouts and Exercises, and serve a slot like Core ones.
2. For each tiered activity, list what the Bank can't serve:
   - a tiered activity with no Workout of that `sport`;
   - a Primary ride, run or swim with no Ladders, which gets no Quality slot (today, swim);
   - Workouts whose `equipment` has a tag no Place has. `smart-trainer` on a `delivery: workout` ride doesn't count: the ride is pushed as outdoor instead. On a `delivery: note` Workout it does count (the FTP test, if ride is Primary);
   - Add-ons only if ride, run or swim is tiered, because an Add-on follows an Endurance Session.
   - Strength is served by Exercises, not Workouts: run `grep -rH '^pattern:\|^equipment:' bank/exercises athlete/bank/exercises`. It's a gap only for a pattern (squat, hinge, push, pull, carry, core) with no Exercise that any Place's Equipment fits.
3. Tell the user each gap in a line. For each one a Personal Workout or Exercise could close (their own routine, a machine at their gym), offer `/add-workout` for it. Run it now if they accept, then re-check that gap.
4. List the gaps that remain for the profile's Notes, and tell the user the Check-in will flag them whenever a slot can't be filled. A gap is closed only by a Personal file that passed `/add-workout`.

**Done when** every tiered activity is servable, by Core or Personal files, or has its remaining gaps listed.

## 4. Week Templates

1. Generate Light, Normal and Push with the generation rules in `docs/planning-rules.md`, in their order. Mark each day that isn't at the default Place with ` @<place>` (rule 5).
2. Show the table, plus one bullet per rule saying how it was applied, as in the examples.
3. Iterate until the user approves.
4. Write `athlete/profile.md` in the format of `docs/athlete-profile.md`: the frontmatter, the approved `## Week Templates` table with its bullets, and `## Notes` with the gaps from step 3 and the unknown values from step 2. On a first run, write `setup` as `sync_verified: no` and `strava_connected: no`. On a re-run, keep the existing `setup` values.
5. Commit it in the athlete repo (`git -C athlete`) as "Setup: profile".

**Done when** the user has approved all three templates, every cell follows the cell syntax in `docs/athlete-profile.md`, and the commit exists.

## 5. intervals.icu

First run `./scripts/icu.py whoami`. If it prints "authenticated as", skip the account, athlete ID and API key below.

1. **Account:** if they have none, open `https://intervals.icu` to sign up. Then enter any FTP, LTHR and max HR from step 2 at `https://intervals.icu/settings`.
2. **MyWhoosh,** only if a Place has `smart-trainer` and `setup.sync_verified` isn't `yes`: open `https://www.mywhoosh.com`. They sign in, open the account's connection settings (look for Connections or Integrations), choose intervals.icu and approve access with the same account. Planned rides sync to MyWhoosh 7 days ahead, and finished rides come back.
3. **Strava,** unless `setup.strava_connected` is `yes`: open `https://intervals.icu/settings`, and they check the 3rd party connections section. Tell them not to disconnect it: that can remove imported history. Record the answer in `setup.strava_connected`.
4. **Athlete ID:** on the same settings page, under Developer Settings at the bottom (it looks like `i12345`). The ID isn't secret, so they can type it in the chat. Set these two lines in `.env`, keeping any others:

   ```
   INTERVALS_ATHLETE_ID=<id>
   INTERVALS_KEYCHAIN_SERVICE=local.slow-burn.intervals-icu
   ```

5. **API key:** in Developer Settings they create a key if there's none, and copy it. Give them this command to type into the prompt, exactly as is, and tell them to paste the key only at the password prompt it shows:

   ```
   ! security add-generic-password -U -a "$USER" -s local.slow-burn.intervals-icu -w
   ```

   If no prompt appears, or the command hangs or fails, they press Escape and run the same command without the `! ` in a separate Terminal window. Confirm the key is stored with `security find-generic-password -a "$USER" -s local.slow-burn.intervals-icu >/dev/null && echo stored`. Leave out `-w`, which would print the key.
6. **Check:** run `./scripts/icu.py whoami`. If the IDs disagree, fix `.env` from what it says.

**Done when** `whoami` prints "authenticated as" with no mismatch, and `setup.strava_connected` is recorded.

## 6. Calendar feed

Skip this if `setup.sync_verified` is `yes` and the user didn't ask for it.

1. Open `https://intervals.icu/calendar`. They click Options → Export Calendar and copy the feed link. It works without a login, so it goes straight into their calendar app, not into the chat.
2. They subscribe to it in their calendar app (look for "subscribe", "add calendar from URL" or "from internet"), name it Training, and pick the shortest refresh interval offered. In Apple Calendar, for example: File → New Calendar Subscription…, paste, Subscribe.

**Done when** the user says the Training calendar is subscribed.

## 7. Test

Skip this if `setup.sync_verified` is `yes` and the user didn't ask for it.

1. Run `./scripts/icu.py test-ride <tomorrow>`. It prints the event ID.
2. Ask them to check that "Setup test (delete me)" is on tomorrow in their calendar, after a refresh, and in the MyWhoosh calendar if they have a smart trainer. It can take a few minutes.
3. Run `./scripts/icu.py delete-event <id>`.
4. Set `setup.sync_verified` to `yes` if it arrived everywhere it should, otherwise `no`, and note in the profile's Notes where it was missing. Commit `athlete/profile.md` as "Setup: intervals.icu".

**Done when** the test event is deleted, `setup.sync_verified` is recorded and committed. Finish by telling the user that `/checkin` plans their first week.
