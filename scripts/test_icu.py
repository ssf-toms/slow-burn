"""Tests for icu.py. Run with: python3 -m unittest discover -s scripts"""
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import icu  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_WEEK = ROOT / "examples" / "2026-W44.md"
EXAMPLES = ROOT / "examples"
EQUIPMENT_TAGS = {"bodyweight", "bands", "band-anchor", "kettlebell", "dumbbells", "barbell",
                  "bench", "cable", "pull-up-bar", "smart-trainer", "pool", "hr-strap"}
PATTERNS = {"squat", "hinge", "push", "pull", "carry", "core", "mobility"}


def athlete_dir(test, profile_text):
    """Point ATHLETE_DIR at a temp dir holding `profile_text` as profile.md."""
    d = tempfile.mkdtemp()
    test.addCleanup(shutil.rmtree, d)
    if profile_text is not None:
        Path(d, "profile.md").write_text(profile_text)
    patcher = mock.patch.dict(os.environ, {"ATHLETE_DIR": d})
    patcher.start()
    test.addCleanup(patcher.stop)
    return Path(d)


def example_profile(name="profile.md"):
    return (EXAMPLES / name).read_text()


class AthleteProfile(unittest.TestCase):
    def test_reads_the_profile_from_athlete_dir(self):
        athlete_dir(self, example_profile("profile-home.md"))
        p = icu.load_profile()
        self.assertEqual(p["places"], {"home": ["bodyweight", "dumbbells"]})
        self.assertEqual(p["tiers"], {"pt": "primary", "strength": "secondary", "walk": "occasional"})
        self.assertEqual(p["availability"]["fixed"], {"Thu": "other:pilates"})
        self.assertEqual(p["pairings"], ["pt+strength"])
        self.assertEqual(p["other"][0], {"id": "pilates", "name": "Pilates class",
                                         "minutes": "45", "counts_as": "training"})
        self.assertEqual(p["setup"], {"sync_verified": "no", "strava_connected": "no"})

    def test_reads_quoted_pace_and_empty_lists(self):
        athlete_dir(self, example_profile())
        p = icu.load_profile()
        self.assertEqual(p["easy_run_pace"], "5:20–5:40/km")
        self.assertEqual(p["other"], [])
        self.assertEqual(p["availability"], {"days_per_week": "6", "fixed": {"Mon": "rest"}})

    def test_missing_profile_says_to_run_setup(self):
        athlete_dir(self, None)
        with self.assertRaisesRegex(icu.PlanError, "run /setup"):
            icu.load_profile()

    def test_defaults_to_the_athlete_folder(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(icu.athlete_dir(), ROOT / "athlete")


class BankFrontmatter(unittest.TestCase):
    def setUp(self):
        self.bank = icu.load_bank()

    def test_exercises_load_with_their_pattern_and_cue(self):
        e = self.bank["kb-goblet-squat"]
        self.assertEqual((e["kind"], e["pattern"], e["reps"]), ("exercise", "squat", "10"))
        self.assertEqual(e["equipment"], ["kettlebell"])
        self.assertTrue(e["cue"])
        self.assertNotIn("Progress:", e["cue"])

    def test_every_exercise_has_a_pattern_an_amount_a_cue_and_a_progress_line(self):
        exercises = {k: e for k, e in self.bank.items() if e["kind"] == "exercise"}
        self.assertGreater(len(exercises), 40)
        for xid, e in exercises.items():
            with self.subTest(exercise=xid):
                self.assertIn(e["pattern"], PATTERNS)
                self.assertEqual(("reps" in e) + ("hold" in e), 1)
                self.assertTrue(e["cue"])
                self.assertIn("\nProgress: ", e["prose"])

    def test_anchored_band_moves_need_the_anchor_tag(self):
        for xid in ("pallof-press", "band-face-pull", "band-row"):
            with self.subTest(exercise=xid):
                self.assertIn("band-anchor", self.bank[xid]["equipment"])

    def test_each_pattern_has_options_for_each_home_equipment_set(self):
        for kit in ("bodyweight", "kettlebell", "dumbbells"):
            for pattern in PATTERNS - {"mobility"}:
                with self.subTest(kit=kit, pattern=pattern):
                    self.assertTrue(any(e["pattern"] == pattern and e["equipment"] == [kit]
                                        for e in self.bank.values() if e["kind"] == "exercise"))

    def test_an_exercise_and_a_workout_cannot_share_an_id(self):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d)
        for sub in ("exercises", "recovery"):
            (d / sub).mkdir()
        shutil.copy(ROOT / "bank" / "recovery" / "rec-walk.md", d / "recovery")
        (d / "exercises" / "rec-walk.md").write_text(
            '---\nid: rec-walk\nname: Walk\npattern: carry\nequipment: []\nreps: "1"\n---\n\nWalk.\n')
        with self.assertRaisesRegex(icu.PlanError, "duplicate Bank ID rec-walk"):
            icu.load_bank(d)

    def test_every_workout_lists_its_equipment_from_the_known_tags(self):
        for wid, w in self.bank.items():
            with self.subTest(workout=wid):
                self.assertIsInstance(w.get("equipment"), list)
                self.assertLessEqual(set(w["equipment"]), EQUIPMENT_TAGS)

    def test_rides_need_a_smart_trainer_and_runs_need_nothing(self):
        self.assertEqual(self.bank["ss-2"]["equipment"], ["smart-trainer"])
        self.assertEqual(self.bank["run-easy-6-8"]["equipment"], [])
        self.assertEqual(self.bank["pt"]["equipment"], [])

    def test_endurance_rides_runs_and_swims_name_alternatives_in_other_sports(self):
        for wid, w in self.bank.items():
            if w["kind"] == "endurance" and w["sport"] in ("ride", "run", "swim"):
                with self.subTest(workout=wid):
                    self.assertNotIn("run_alternative", w)
                    alts = icu.alternatives_of(w)
                    self.assertTrue(alts)
                    for a in alts:
                        self.assertIn(a, self.bank)
                        self.assertNotEqual(self.bank[a]["sport"], w["sport"])

    def test_every_workout_is_a_known_sport(self):
        sports = {"ride", "run", "swim", "walk", "strength", "pt"}
        for wid, w in self.bank.items():
            with self.subTest(workout=wid):
                self.assertIn(w["sport"], sports)

    def test_swims_need_a_pool_and_are_notes(self):
        swims = [w for w in self.bank.values() if w["sport"] == "swim"]
        self.assertGreaterEqual(len(swims), 3)
        for w in swims:
            with self.subTest(workout=w["id"]):
                self.assertEqual((w["equipment"], w["delivery"]), (["pool"], "note"))

    def test_run_workouts_use_the_pace_placeholder(self):
        for wid in ("run-easy-6-8", "run-easy-8-10", "run-easy-10-12"):
            with self.subTest(workout=wid):
                self.assertIn("{easy_run_pace}", self.bank[wid]["prose"])
                self.assertNotIn("5:45", self.bank[wid]["prose"])


# An indoor rider like the one examples/2026-W44.md was planned for.
INDOOR_PROFILE = """---
tiers:
  ride: primary
  run: secondary
  strength: secondary
  pt: secondary
other: []
places:
  home: [bodyweight, bands, kettlebell, smart-trainer]
experience: some
availability:
  days_per_week: 6
  fixed: {}
easy_run_pace: "5:45–6:00/km"
pairings: [pt+strength]
alternatives: on
ftp: 250
setup:
  sync_verified: yes
  strava_connected: yes
---
"""


def week(test, rows, level="normal"):
    """Write a 2026-W45 Week Record. `rows` maps day to (Session, Workout[, Add-on])."""
    lines = []
    for i, day in enumerate(icu.DAYS):
        session, workouts, addon = (tuple(rows.get(day, ("Recovery", ""))) + ("",))[:3]
        lines.append(f"| {day} | 11-{2 + i:02d} | {session} | {workouts} | {addon} | |")
    text = (f"---\nweek: 2026-W45\nstart: 2026-11-02\nlevel: {level}\nload_warning: none\n---\n\n"
            "## Plan\n\n| Day | Date | Session | Workout | Add-on | Done |\n|---|---|---|---|---|---|\n"
            + "\n".join(lines) + "\n")
    d = tempfile.mkdtemp()
    test.addCleanup(shutil.rmtree, d)
    path = Path(d, "2026-W45.md")
    path.write_text(text)
    return path


def build(path, bank=None):
    fm, days = icu.parse_week(path)
    return icu.build_events(fm, days, bank or icu.load_bank(), icu.load_profile())


def event(events, day):
    return next(e for e in events if e["external_id"] == f"tp-2026-W45-{day}")


def dry_run(path):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        icu.cmd_push_week(str(path), dry_run=True)
    return out.getvalue()


class PushWeekDryRun(unittest.TestCase):
    def setUp(self):
        athlete_dir(self, INDOOR_PROFILE)

    def test_example_week_has_no_plan_problems(self):
        fm, days = icu.parse_week(EXAMPLE_WEEK)
        _events, problems = icu.build_events(fm, days, icu.load_bank(), icu.load_profile())
        self.assertEqual(problems, [])

    def test_endurance_ride_description_offers_its_alternative(self):
        fm, days = icu.parse_week(EXAMPLE_WEEK)
        events, _ = icu.build_events(fm, days, icu.load_bank(), icu.load_profile())
        wed = next(e for e in events if e["external_id"] == "tp-2026-W44-Wed")
        self.assertIn("Alternative: Easy run 8–10 km", wed["description"])
        self.assertNotIn("swap this for", wed["description"])  # Bank-only link line

    def test_dry_run_prints_the_events_without_credentials(self):
        self.assertIn("dry run: 10 to upsert", dry_run(EXAMPLE_WEEK))


class ExampleProfileWeeks(unittest.TestCase):
    def test_week_for_the_outdoor_triathlete_passes(self):
        athlete_dir(self, example_profile("profile.md"))
        self.assertIn("dry run: 6 to upsert", dry_run(EXAMPLES / "profile-2026-W45.md"))

    def test_week_for_the_home_athlete_passes(self):
        athlete_dir(self, example_profile("profile-home.md"))
        out = dry_run(EXAMPLES / "profile-home-2026-W45.md")
        self.assertIn("dry run: 8 to upsert", out)
        self.assertIn("2026-11-02  NOTE    PT routine + Strength (3 rounds)", out)
        self.assertIn("2026-11-06  NOTE    PT routine + Strength (3 rounds)", out)

    def test_week_for_the_two_place_athlete_passes(self):
        athlete_dir(self, example_profile("profile-gym.md"))
        out = dry_run(EXAMPLES / "profile-gym-2026-W45.md")
        self.assertIn("dry run: 7 to upsert", out)
        self.assertIn("2026-11-02  NOTE    Strength (3 rounds)", out)
        self.assertIn("2026-11-04  NOTE    Strength (3 rounds)", out)

    def test_the_two_place_templates_have_a_gym_day(self):
        text = example_profile("profile-gym.md")
        fixed = icu.split_frontmatter(text)[0]["availability"]["fixed"]
        self.assertEqual(fixed, {"Wed": "strength @gym"})
        wed = next(l for l in text.splitlines() if l.startswith("| Wed |"))
        self.assertEqual(wed.count("Strength: strength @gym"), 3)

    def test_triathlete_normal_week_with_a_run_ladder_step_and_run_alternative(self):
        athlete_dir(self, example_profile("profile.md"))
        path = week(self, {"Mon": ("Recovery", ""), "Tue": ("Quality", "th-2"),
                           "Wed": ("Endurance", "end-ride-60"), "Thu": ("Quality", "run-th-2"),
                           "Fri": ("Recovery", ""), "Sun": ("Endurance", "run-easy-8-10")})
        self.assertIn("dry run: 6 to upsert", dry_run(path))

    def test_run_test_day_passes_for_the_triathlete(self):
        athlete_dir(self, example_profile("profile.md"))
        events, problems = build(week(self, {"Thu": ("Test", "run-test-20")}))
        self.assertEqual(problems, [])
        self.assertIn("4:50/km", event(events, "Thu")["description"])

    def test_dumbbell_only_athlete_cannot_do_a_kettlebell_exercise(self):
        athlete_dir(self, example_profile("profile-home.md"))
        path = week(self, {"Mon": ("Strength", "pt, kb-swing, db-goblet-squat, push-up")})
        with self.assertRaises(SystemExit) as cm:
            dry_run(path)
        self.assertIn("Mon: kb-swing needs kettlebell (not at home)",
                      str(cm.exception))

    def test_pallof_press_fails_clearly_without_a_band_anchor(self):
        banded = example_profile("profile-home.md").replace("[bodyweight, dumbbells]",
                                                             "[bodyweight, dumbbells, bands]")
        athlete_dir(self, banded)
        path = week(self, {"Mon": ("Strength", "pt, db-goblet-squat, db-rdl, band-pull-apart, pallof-press")})
        with self.assertRaises(SystemExit) as cm:
            dry_run(path)
        self.assertIn("Mon: pallof-press needs band-anchor (not at home)",
                      str(cm.exception))
        self.assertNotIn("band-pull-apart", str(cm.exception))  # bands alone is enough for it


class ProfileChecks(unittest.TestCase):
    def problems(self, profile, rows, level="normal"):
        athlete_dir(self, profile)
        return build(week(self, rows, level))[1]

    def test_add_on_equipment_is_checked_too(self):
        home = example_profile("profile-home.md").replace("[bodyweight, dumbbells]", "[bodyweight, bands]")
        athlete_dir(self, home.replace("  walk: occasional", "  walk: occasional\n  run: primary"))
        problems = build(week(self, {"Wed": ("Endurance", "run-easy-6-8", "band-pull-apart, kb-halo")}))[1]
        self.assertIn("Wed: kb-halo needs kettlebell (not at home)", problems)
        self.assertFalse(any("band-pull-apart" in p for p in problems))

    def test_rides_need_no_smart_trainer_to_be_planned(self):
        self.assertEqual(self.problems(example_profile(), {"Tue": ("Quality", "th-2")}), [])

    def test_the_ftp_test_still_needs_a_smart_trainer(self):
        problems = self.problems(example_profile(), {"Tue": ("Test", "ftp-ramp-test, test-spin")})
        self.assertIn("Tue: ftp-ramp-test needs smart-trainer (not at home)", problems)

    def test_a_swim_needs_a_pool_at_the_days_place(self):
        problems = self.problems(example_profile(), {"Sat": ("Endurance", "swim-easy-1500")})
        self.assertEqual(problems, ["Sat: swim-easy-1500 needs pool (not at home)"])
        self.assertEqual(self.problems(example_profile(), {"Sat": ("Endurance @gym", "swim-easy-1500")}), [])

    def test_allowed_pairing_passes_in_either_order(self):
        strength = "kb-goblet-squat, kb-swing, push-up, band-pull-apart, kb-suitcase-carry, dead-bug"
        for workouts in (f"pt, {strength}", f"{strength}, pt"):
            with self.subTest(workouts=workouts):
                self.assertEqual(self.problems(INDOOR_PROFILE, {"Mon": ("Strength", workouts)}), [])

    def test_pairing_must_be_in_the_profile(self):
        problems = self.problems(INDOOR_PROFILE, {"Mon": ("Recovery", "pt, rec-walk")})
        self.assertIn("Mon: pt + walk is not an allowed pairing (profile pairings: pt+strength)", problems)

    def test_nothing_pairs_with_a_quality_session(self):
        problems = self.problems(INDOOR_PROFILE.replace("[pt+strength]", "[pt+strength, ride+pt]"),
                                 {"Tue": ("Quality", "th-2, pt")})
        self.assertIn("Tue: nothing can be paired with a Quality Session", problems)

    def test_ftp_test_row_is_not_a_pairing(self):
        self.assertEqual(self.problems(INDOOR_PROFILE, {"Tue": ("Test", "ftp-ramp-test, test-spin")}), [])

    def test_unknown_other_activity_is_reported(self):
        problems = self.problems(example_profile("profile-home.md"), {"Thu": ("Other", "other:salsa")})
        self.assertIn("Thu: other:salsa is not in the profile's other activities", problems)

    def test_other_activities_are_never_paired(self):
        problems = self.problems(example_profile("profile-home.md"), {"Thu": ("Other", "pt, other:pilates")})
        self.assertIn("Thu: other activities can't be paired", problems)

    def test_unknown_session_kind_is_still_reported(self):
        problems = self.problems(INDOOR_PROFILE, {"Thu": ("Tempo", "pt")})
        self.assertIn("Thu: unknown Session 'Tempo'", problems)

    def test_run_needs_a_pace_in_the_profile(self):
        no_run = example_profile("profile-home.md")
        problems = self.problems(no_run, {"Wed": ("Endurance", "run-easy-6-8")})
        self.assertIn("Wed: run-easy-6-8 needs easy_run_pace in the profile", problems)


    def test_run_quality_needs_a_threshold_pace_in_the_profile(self):
        no_threshold = re.sub(r"threshold_run_pace: .*\n", "", example_profile())
        problems = self.problems(no_threshold, {"Tue": ("Quality", "run-tempo-1")})
        self.assertIn("Tue: run-tempo-1 needs threshold_run_pace in the profile", problems)

class PushedEvents(unittest.TestCase):
    def events(self, profile, rows, level="normal", bank=None):
        athlete_dir(self, profile)
        events, problems = build(week(self, rows, level), bank)
        self.assertEqual(problems, [])
        return events

    def test_other_activity_is_pushed_as_a_note(self):
        e = event(self.events(example_profile("profile-home.md"), {"Thu": ("Other", "other:pilates")}), "Thu")
        self.assertEqual((e["category"], e["name"]), ("NOTE", "Pilates class"))
        self.assertIn("45 min", e["description"])

    def test_run_pace_comes_from_the_profile(self):
        e = event(self.events(example_profile(), {"Wed": ("Endurance", "run-easy-6-8")}), "Wed")
        self.assertIn("Easy pace (5:20–5:40/km)", e["description"])

    def test_run_quality_note_gets_threshold_pace_from_the_profile(self):
        e = event(self.events(example_profile(), {"Tue": ("Quality", "run-th-2")}), "Tue")
        self.assertEqual(e["category"], "NOTE")
        self.assertIn("4:50/km", e["description"])
        self.assertNotIn("{threshold_run_pace}", e["description"])

    def test_swim_is_pushed_as_a_note(self):
        e = event(self.events(example_profile(), {"Sat": ("Endurance @gym", "swim-steady-2000")}), "Sat")
        self.assertEqual((e["category"], e["name"]), ("NOTE", "Steady swim 2000 m"))
        self.assertIn("Main set", e["description"])

    def test_dose_for_the_week_level_is_appended(self):
        bank = icu.load_bank()
        bank["pt"] = {**bank["pt"], "dose": {"light": "2 rounds", "normal": "3 rounds", "push": "4 rounds"}}
        e = event(self.events(INDOOR_PROFILE, {"Fri": ("Recovery", "pt")}, "light", bank), "Fri")
        self.assertTrue(e["description"].endswith("Today: 2 rounds"))

    def test_no_dose_line_without_a_dose(self):
        e = event(self.events(INDOOR_PROFILE, {"Fri": ("Recovery", "pt")}), "Fri")
        self.assertNotIn("Today:", e["description"])

    def test_rides_are_indoor_only_with_a_smart_trainer(self):
        indoor = event(self.events(INDOOR_PROFILE, {"Tue": ("Quality", "th-2")}), "Tue")
        outdoor = event(self.events(example_profile(), {"Tue": ("Quality", "th-2")}), "Tue")
        self.assertIs(indoor["indoor"], True)
        self.assertIs(outdoor["indoor"], False)

    def test_alternative_line_only_when_alternatives_are_on(self):
        off = INDOOR_PROFILE.replace("alternatives: on\n", "")
        e = event(self.events(off, {"Wed": ("Endurance", "end-ride-60")}), "Wed")
        self.assertNotIn("Alternative:", e["description"])

    def test_no_alternative_line_when_its_sport_is_not_tiered(self):
        no_run = INDOOR_PROFILE.replace("  run: secondary\n", "").replace('easy_run_pace: "5:45–6:00/km"\n', "")
        e = event(self.events(no_run, {"Wed": ("Endurance", "end-ride-60")}), "Wed")
        self.assertNotIn("Alternative:", e["description"])

    def test_no_alternative_line_when_its_equipment_is_missing(self):
        bank = icu.load_bank()
        bank["run-easy-8-10"] = {**bank["run-easy-8-10"], "equipment": ["pool"]}
        e = event(self.events(INDOOR_PROFILE, {"Wed": ("Endurance", "end-ride-60")}, bank=bank), "Wed")
        self.assertNotIn("Alternative:", e["description"])

    def test_alternative_line_when_its_sport_is_tiered_and_equipment_fits(self):
        e = event(self.events(INDOOR_PROFILE, {"Wed": ("Endurance", "end-ride-60")}), "Wed")
        self.assertIn("Alternative: Easy run 8–10 km", e["description"])


    def test_run_note_offers_its_ride_alternative(self):
        e = event(self.events(example_profile(), {"Wed": ("Endurance", "run-easy-8-10")}), "Wed")
        self.assertEqual(e["category"], "NOTE")
        self.assertIn("Alternative: Endurance 60.", e["description"])
        self.assertNotIn("swap this for", e["description"])

    def test_triathletes_light_ride_offers_a_swim_alternative(self):
        e = event(self.events(example_profile(), {"Fri": ("Endurance", "end-ride-50")}, "light"), "Fri")
        self.assertIn("Alternative: Easy swim 1500 m.", e["description"])
        self.assertNotIn("Alternative: Easy run", e["description"])

    def test_first_alternative_the_profile_can_use_is_offered(self):
        e = event(self.events(INDOOR_PROFILE, {"Fri": ("Endurance", "end-ride-50")}, "light"), "Fri")
        self.assertIn("Alternative: Easy run 6–8 km.", e["description"])
        self.assertNotIn("swim", e["description"])

    def test_swim_offers_its_first_alternative_that_fits(self):
        e = event(self.events(example_profile(), {"Sat": ("Endurance @gym", "swim-easy-1500")}), "Sat")
        self.assertIn("Alternative: Easy run 5–6 km.", e["description"])

    def test_run_alternative_line_only_when_alternatives_are_on(self):
        off = example_profile().replace("alternatives: on\n", "")
        e = event(self.events(off, {"Wed": ("Endurance", "run-easy-8-10")}), "Wed")
        self.assertNotIn("Alternative:", e["description"])


HOME_STRENGTH = "db-goblet-squat, db-rdl, push-up, db-row, db-suitcase-carry, dead-bug"


class ComposedStrength(unittest.TestCase):
    def build(self, rows, level="normal", profile=None):
        athlete_dir(self, profile or example_profile("profile-home.md"))
        return build(week(self, rows, level))

    def test_a_strength_row_is_one_note_listing_each_exercise(self):
        events, problems = self.build({"Mon": ("Strength", f"pt, {HOME_STRENGTH}")})
        self.assertEqual(problems, [])
        e = event(events, "Mon")
        self.assertEqual(e["name"], "PT routine + Strength (3 rounds)")
        self.assertIn("- Goblet squat (dumbbell) × 10: Hold one dumbbell upright at your chest",
                      e["description"])
        self.assertIn("- Dumbbell suitcase carry × 40 s/side: Dumbbell in one hand", e["description"])
        self.assertNotIn("Progress:", e["description"])

    def test_rounds_come_from_the_week_level(self):
        for level, rounds in (("light", 2), ("normal", 3), ("push", 4)):
            with self.subTest(level=level):
                events, _ = self.build({"Mon": ("Strength", HOME_STRENGTH)}, level)
                e = event(events, "Mon")
                self.assertEqual(e["name"], f"Strength ({rounds} rounds)")
                self.assertTrue(e["description"].startswith(f"{rounds} rounds"))

    def test_an_add_on_is_its_own_composed_note(self):
        events, problems = self.build({"Wed": ("Endurance", "end-ride-60", "kb-swing, band-pull-apart, dead-bug")},
                                      "light", INDOOR_PROFILE)
        self.assertEqual(problems, [])
        e = next(e for e in events if e["external_id"] == "tp-2026-W45-Wed-addon")
        self.assertEqual(e["name"], "Add-on (2 rounds)")
        self.assertIn("- Band pull-apart × 15: Arms straight", e["description"])

    def test_the_add_on_cell_holds_only_exercises(self):
        problems = self.build({"Wed": ("Endurance", "end-ride-60", "pt, kb-swing, dead-bug")},
                              profile=INDOOR_PROFILE)[1]
        self.assertIn("Wed: the Add-on holds Exercises only, not pt", problems)

    def test_a_strength_block_has_3_to_8_exercises(self):
        problems = self.build({"Mon": ("Strength", "pt, db-goblet-squat, db-row")})[1]
        self.assertIn("Mon: a Strength block needs 3–8 Exercises, has 2", problems)
        nine = HOME_STRENGTH + ", air-squat, glute-bridge, prone-ytw"
        self.assertIn("Mon: a Strength block needs 3–8 Exercises, has 9",
                      self.build({"Mon": ("Strength", nine)})[1])

    def test_an_add_on_has_2_to_4_exercises(self):
        problems = self.build({"Wed": ("Endurance", "end-ride-60", "dead-bug")}, profile=INDOOR_PROFILE)[1]
        self.assertIn("Wed: an Add-on needs 2–4 Exercises, has 1", problems)

    def test_an_exercise_is_not_repeated_within_a_row(self):
        problems = self.build({"Wed": ("Endurance", "end-ride-60", "dead-bug, kb-swing, dead-bug")},
                              profile=INDOOR_PROFILE)[1]
        self.assertIn("Wed: dead-bug is in the row twice", problems)

    def test_exercises_in_a_workout_cell_are_consecutive(self):
        problems = self.build({"Mon": ("Strength", "db-goblet-squat, db-rdl, push-up, pt, db-row, dead-bug, air-squat")})[1]
        self.assertIn("Mon: a Workout cell has one block of consecutive Exercises", problems)


class Extensions(unittest.TestCase):
    def setUp(self):
        athlete_dir(self, INDOOR_PROFILE)

    def build(self, rows, level="push"):
        return build(week(self, rows, level))

    def test_push_quality_ride_gets_endurance_minutes_before_the_cooldown(self):
        events, problems = self.build({"Tue": ("Quality", "th-2 +15")})
        self.assertEqual(problems, [])
        e = event(events, "Tue")
        self.assertEqual(e["name"], "Threshold 2: 3×8 min @ 97% +15′")
        self.assertIn("Extension\n- 15m 68%\n\nCooldown\n- 6m 50%", e["description"])
        self.assertIn("Today: +15 min at Endurance (68%) before the cooldown.", e["description"])

    def test_extensions_are_for_push_weeks_only(self):
        problems = self.build({"Tue": ("Quality", "th-2 +15")}, "normal")[1]
        self.assertIn("Tue: th-2 +15: Extensions are for Push weeks only", problems)

    def test_only_quality_rides_can_be_extended(self):
        problems = self.build({"Wed": ("Endurance", "end-ride-60 +10")})[1]
        self.assertIn("Wed: end-ride-60 +10: only a Quality ride can have an Extension", problems)

    def test_extension_length_is_bounded(self):
        problems = self.build({"Tue": ("Quality", "th-2 +30")})[1]
        self.assertIn("Tue: th-2 +30: an Extension is 10–15 min", problems)

    def test_at_most_one_extension_a_week(self):
        problems = self.build({"Tue": ("Quality", "th-2 +10"), "Thu": ("Quality", "ss-2 +10")})[1]
        self.assertIn("at most one Extension a week", problems)


class DoseByLevel(unittest.TestCase):
    def setUp(self):
        athlete_dir(self, INDOOR_PROFILE)

    def test_normal_week_can_have_a_75_minute_ride(self):
        problems = build(week(self, {"Sat": ("Endurance", "end-ride-75")}, "normal"))[1]
        self.assertEqual(problems, [])

    def test_progressive_75_stays_push_only(self):
        problems = build(week(self, {"Sat": ("Endurance", "end-ride-75-progressive")}, "normal"))[1]
        self.assertIn("Sat: end-ride-75-progressive is for push weeks only", problems)


class SetupCommands(unittest.TestCase):
    def run_cmd(self, argv, reply=None):
        out = io.StringIO()
        with mock.patch.object(icu, "ATHLETE", "i123456"), \
                mock.patch.object(icu, "call", return_value=reply) as call, \
                contextlib.redirect_stdout(out):
            icu.main(["icu.py", *argv])
        return out.getvalue(), call

    def test_whoami_prints_name_and_id(self):
        out, call = self.run_cmd(["whoami"], {"id": "i123456", "name": "Sam Rider"})
        call.assert_called_once_with("GET", "", None, "0")  # "0": whoever owns the key
        self.assertEqual(out, "authenticated as Sam Rider (i123456)\n")

    def test_whoami_fails_when_the_id_differs_from_env(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_cmd(["whoami"], {"id": "i999", "name": "Sam Rider"})
        self.assertIn("API says your athlete ID is i999, not i123456", str(cm.exception))

    def test_test_ride_creates_a_ride_and_prints_its_id(self):
        out, call = self.run_cmd(["test-ride", "2026-11-01"], {"id": 4242})
        method, path, body = call.call_args.args
        self.assertEqual((method, path), ("POST", "/events"))
        self.assertEqual((body["category"], body["type"], body["name"]),
                         ("WORKOUT", "Ride", "Setup test (delete me)"))
        self.assertEqual(body["start_date_local"], "2026-11-01T00:00:00")
        self.assertEqual(out, "4242\n")

    def test_delete_event(self):
        out, call = self.run_cmd(["delete-event", "4242"])
        call.assert_called_once_with("DELETE", "/events/4242")
        self.assertEqual(out, "deleted event 4242\n")


TWO_PLACES = """---
tiers:
  ride: secondary
  strength: primary
other: []
places:
  home: [bodyweight, dumbbells]
  gym: [barbell, dumbbells, cable, pull-up-bar, bench, smart-trainer]
availability:
  days_per_week: 4
  fixed:
    Wed: strength @gym
ftp: 200
setup:
  sync_verified: no
  strava_connected: no
---
"""
GYM_STRENGTH = "back-squat, deadlift, bench-press, cable-row, db-suitcase-carry, hanging-knee-raise"


class Places(unittest.TestCase):
    def build(self, rows, profile=TWO_PLACES):
        athlete_dir(self, profile)
        return build(week(self, rows))

    def test_places_map_reads_in_order_with_fixed_place_days(self):
        athlete_dir(self, TWO_PLACES)
        p = icu.load_profile()
        self.assertEqual(list(p["places"]), ["home", "gym"])
        self.assertEqual(p["places"]["gym"], ["barbell", "dumbbells", "cable", "pull-up-bar",
                                              "bench", "smart-trainer"])
        self.assertEqual(p["availability"]["fixed"], {"Wed": "strength @gym"})

    def test_a_gym_day_accepts_a_barbell_exercise(self):
        self.assertEqual(self.build({"Wed": ("Strength @gym", GYM_STRENGTH)})[1], [])

    def test_a_home_day_rejects_a_barbell_exercise(self):
        problems = self.build({"Mon": ("Strength", GYM_STRENGTH)})[1]
        self.assertIn("Mon: back-squat needs barbell (not at home)", problems)
        self.assertNotIn("db-suitcase-carry", " ".join(problems))  # dumbbells are at home too

    def test_an_unknown_place_is_an_error(self):
        athlete_dir(self, TWO_PLACES)
        with self.assertRaises(SystemExit) as cm:
            dry_run(week(self, {"Wed": ("Strength @pool", GYM_STRENGTH)}))
        self.assertIn("Wed: unknown Place '@pool' (profile places: home, gym)", str(cm.exception))

    def test_a_ride_is_indoor_only_at_a_place_with_a_smart_trainer(self):
        events, problems = self.build({"Tue": ("Quality", "th-2"), "Thu": ("Quality @gym", "ss-2")})
        self.assertEqual(problems, [])
        self.assertIs(event(events, "Tue")["indoor"], False)
        self.assertIs(event(events, "Thu")["indoor"], True)

    def test_an_alternative_may_be_at_another_place(self):
        pool = TWO_PLACES.replace("  ride: secondary\n", "  ride: secondary\n  swim: secondary\n")
        pool = pool.replace("smart-trainer]\n", "smart-trainer, pool]\nalternatives: on\n")
        events, problems = self.build({"Fri": ("Endurance", "end-ride-50")}, pool)
        self.assertEqual(problems, [])
        self.assertIn("Alternative: Easy swim 1500 m.", event(events, "Fri")["description"])

    def test_the_old_equipment_list_asks_for_places(self):
        flat = re.sub(r"places:\n(  .*\n)+", "equipment: [bodyweight, dumbbells]\n", TWO_PLACES)
        self.assertNotIn("places", flat)
        athlete_dir(self, flat)
        with self.assertRaisesRegex(icu.ProfileError, "`equipment` is now `places`"):
            build(week(self, {"Tue": ("Quality", "th-2")}))


class UsageTest(unittest.TestCase):
    def test_missing_arguments_print_usage(self):
        with self.assertRaises(SystemExit) as cm:
            icu.main(["icu.py", "events", "2026-10-26"])
        self.assertEqual(cm.exception.code, icu.__doc__)


if __name__ == "__main__":
    unittest.main()

