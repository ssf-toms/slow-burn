"""Tests for icu.py. Run with: python3 -m unittest discover -s scripts"""
import contextlib
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import icu  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_WEEK = ROOT / "examples" / "2026-W44.md"
EQUIPMENT_TAGS = {"bodyweight", "bands", "kettlebell", "dumbbells", "barbell",
                  "gym", "smart-trainer", "pool", "hr-strap"}


class BankFrontmatter(unittest.TestCase):
    def setUp(self):
        self.bank = icu.load_bank()

    def test_every_workout_lists_its_equipment_from_the_known_tags(self):
        for wid, w in self.bank.items():
            with self.subTest(workout=wid):
                self.assertIsInstance(w.get("equipment"), list)
                self.assertLessEqual(set(w["equipment"]), EQUIPMENT_TAGS)

    def test_rides_need_a_smart_trainer_and_runs_need_nothing(self):
        self.assertEqual(self.bank["ss-2"]["equipment"], ["smart-trainer"])
        self.assertEqual(self.bank["run-easy-6-8"]["equipment"], [])
        self.assertEqual(self.bank["pt"]["equipment"], [])

    def test_endurance_rides_name_an_alternative_in_the_bank(self):
        for wid, w in self.bank.items():
            if w["kind"] == "endurance" and w["sport"] == "ride":
                with self.subTest(workout=wid):
                    self.assertNotIn("run_alternative", w)
                    self.assertIn(w.get("alternative"), self.bank)

    def test_run_workouts_use_the_pace_placeholder(self):
        for wid in ("run-easy-6-8", "run-easy-8-10", "run-easy-10-12"):
            with self.subTest(workout=wid):
                self.assertIn("{easy_run_pace}", self.bank[wid]["prose"])
                self.assertNotIn("5:45", self.bank[wid]["prose"])


class PushWeekDryRun(unittest.TestCase):
    def test_example_week_has_no_plan_problems(self):
        fm, days = icu.parse_week(EXAMPLE_WEEK)
        _events, problems = icu.build_events(fm, days, icu.load_bank())
        self.assertEqual(problems, [])

    def test_endurance_ride_description_offers_its_alternative(self):
        fm, days = icu.parse_week(EXAMPLE_WEEK)
        events, _ = icu.build_events(fm, days, icu.load_bank())
        wed = next(e for e in events if e["external_id"] == "tp-2026-W44-Wed")
        self.assertIn("Alternative: Easy run 8–10 km", wed["description"])
        self.assertNotIn("swap this for", wed["description"])  # Bank-only link line

    def test_dry_run_prints_the_events_without_credentials(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            icu.cmd_push_week(str(EXAMPLE_WEEK), dry_run=True)
        self.assertIn("dry run: 10 to upsert", out.getvalue())


if __name__ == "__main__":
    unittest.main()
