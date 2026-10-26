#!/usr/bin/env python3
"""intervals.icu client for slow-burn.

Usage:
  icu.py push-week weeks/2026-W44.md [--from YYYY-MM-DD] [--dry-run]
  icu.py clear-week 2026-W44
  icu.py events  YYYY-MM-DD YYYY-MM-DD
  icu.py rides   YYYY-MM-DD YYYY-MM-DD
  icu.py fitness YYYY-MM-DD YYYY-MM-DD

Week Record format: docs/week-records.md. Workout Bank: bank/README.md.
Credentials: INTERVALS_ATHLETE_ID and INTERVALS_KEYCHAIN_SERVICE in .env, API
key in the macOS Keychain (written by scripts/setup-intervals.sh).
"""
import base64
import datetime as dt
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://intervals.icu/api/v1"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SESSION_KINDS = {"Recovery", "Quality", "Endurance", "Test"}


class PlanError(Exception):
    pass


# ── config and HTTP ──────────────────────────────────────────────────────
def load_env():
    env = {}
    for line in (ROOT / ".env").read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")
    return env


ENV = load_env()
ATHLETE = ENV["INTERVALS_ATHLETE_ID"]


def api_key():
    return subprocess.run(
        ["security", "find-generic-password", "-a", subprocess.getoutput("id -un"),
         "-s", ENV["INTERVALS_KEYCHAIN_SERVICE"], "-w"],
        check=True, capture_output=True, text=True).stdout.strip()


def call(method, path, body=None, **query):
    url = f"{API}/athlete/{ATHLETE}{path}"
    if query:
        url += "?" + "&".join(f"{k}={v}" for k, v in query.items())
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    token = base64.b64encode(f"API_KEY:{api_key()}".encode()).decode()
    req.add_header("Authorization", f"Basic {token}")
    req.add_header("User-Agent", "slow-burn/0.1")  # Cloudflare rejects urllib's default
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} failed: HTTP {e.code} {e.read().decode()[:300]}")
    return json.loads(raw) if raw else None


# ── Markdown parsing ─────────────────────────────────────────────────────
def split_frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise PlanError("missing frontmatter")
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        elif len(v) >= 2 and v[0] == v[-1] == '"':
            v = v[1:-1].replace('\\"', '"')
        fm[k.strip()] = v
    return fm, m.group(2)


def load_bank():
    bank = {}
    for p in sorted((ROOT / "bank").rglob("*.md")):
        if p.name == "README.md":
            continue
        fm, body = split_frontmatter(p.read_text())
        block = re.search(r"```intervals\n(.*?)\n```", body, re.S)
        prose = re.sub(r"```intervals\n.*?\n```", "", body, flags=re.S)
        prose = re.sub(r"^# .*\n", "", prose.strip())
        prose = re.sub(r"\n?On a good-weather day, swap this for .*", "", prose).strip()
        bank[fm["id"]] = {**fm, "workout_text": block.group(1) if block else None, "prose": prose}
    return bank


def parse_week(path):
    fm, body = split_frontmatter(Path(path).read_text())
    start = dt.date.fromisoformat(fm["start"])
    if start.weekday() != 0:
        raise PlanError(f"start {start} is not a Monday")
    iso = start.isocalendar()
    if fm["week"] != f"{iso[0]}-W{iso[1]:02d}":
        raise PlanError(f"week {fm['week']} doesn't match start {start}")
    plan = re.search(r"## Plan\n(.*?)(\n## |\Z)", body, re.S)
    if not plan:
        raise PlanError("no ## Plan section")
    rows = [l for l in plan.group(1).splitlines() if l.startswith("|")][2:]
    days = []
    for line in rows:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            raise PlanError(f"expected 6 columns: {line}")
        day, date_s, session, workouts, addon, _done = cells
        date = start + dt.timedelta(days=DAYS.index(day))
        if date_s and date_s != date.strftime("%m-%d"):
            raise PlanError(f"{day}: Date {date_s} should be {date:%m-%d}")
        days.append(dict(day=day, date=date, session=session,
                         workouts=[w.strip() for w in workouts.split(",") if w.strip()],
                         addon=addon or None))
    if [d["day"] for d in days] != DAYS:
        raise PlanError("Plan must list Mon..Sun once each, in order")
    return fm, days


# ── building events ──────────────────────────────────────────────────────
def week_id(date):
    y, w, _ = date.isocalendar()
    return f"{y}-W{w:02d}"


def ext(week, suffix):
    return f"tp-{week}-{suffix}"


def build_events(fm, days, bank):
    week, level = fm["week"], fm["level"]
    events, problems = [], []
    for d in days:
        if not d["session"] and not d["workouts"] and not d["addon"]:
            continue  # unplanned day in a partial week
        if d["session"] not in SESSION_KINDS:
            problems.append(f"{d['day']}: unknown Session '{d['session']}'")
        if d["addon"] and d["session"] not in ("Endurance", "Test"):
            problems.append(f"{d['day']}: Add-on only allowed on Endurance or Test rows")
        missing = [w for w in d["workouts"] + ([d["addon"]] if d["addon"] else []) if w not in bank]
        if missing:
            problems.append(f"{d['day']}: not in Bank: {', '.join(missing)}")
            continue
        ws = [bank[w] for w in d["workouts"]]
        for w in ws:
            if w.get("levels") and level not in w["levels"]:
                problems.append(f"{d['day']}: {w['id']} is for {'/'.join(w['levels'])} weeks only")
        rides = [w for w in ws if w["delivery"] == "workout"]
        if len(rides) > 1:
            problems.append(f"{d['day']}: more than one ride Workout")
        when = f"{d['date']}T00:00:00"
        notes = [w for w in ws if w["delivery"] != "workout"]
        if rides and notes:  # e.g. Test row: MyWhoosh test note + pushed spin
            events.append(dict(category="NOTE", name=" + ".join(w["name"] for w in notes),
                               description="\n\n".join(w["prose"] for w in notes),
                               start_date_local=when, end_date_local=when,
                               external_id=ext(week, f"{d['day']}-note")))
        if rides:
            r = rides[0]
            desc = r["prose"]
            if r.get("run_alternative") in bank:
                alt = bank[r["run_alternative"]]
                desc += f"\n\nGood weather? Run instead: {alt['name']}. {alt['prose']}"
            desc += "\n\n" + r["workout_text"]
            events.append(dict(category="WORKOUT", type="Ride", indoor=True, name=r["name"],
                               description=desc, start_date_local=when,
                               external_id=ext(week, d["day"])))
        elif ws:
            events.append(dict(category="NOTE", name=" + ".join(w["name"] for w in ws),
                               description="\n\n".join(w["prose"] for w in ws),
                               start_date_local=when, end_date_local=when,
                               external_id=ext(week, d["day"])))
        if d["addon"]:
            a = bank[d["addon"]]
            events.append(dict(category="NOTE", name=a["name"], description=a["prose"],
                               start_date_local=when, end_date_local=when,
                               external_id=ext(week, f"{d['day']}-addon")))
    sunday = days[-1]["date"]
    next_week = week_id(sunday + dt.timedelta(days=1))
    events.append(dict(category="NOTE", name="Check-in: plan next week",
                       description="Sunday Check-in with Claude: review this week, pick next week's Level.",
                       start_date_local=f"{sunday}T00:00:00", end_date_local=f"{sunday}T00:00:00",
                       external_id=ext(week, "checkin")))
    monday = sunday + dt.timedelta(days=1)
    events.append(dict(category="NOTE", name="Check-in needed",
                       description="No Week Plan yet for this week. Run the Check-in with Claude.",
                       start_date_local=f"{monday}T00:00:00", end_date_local=f"{monday}T00:00:00",
                       external_id=ext(next_week, "checkin-needed")))
    return events, problems


def all_ext_ids(week, monday):
    """Every external_id push-week may own for a week, with its date."""
    ids = {}
    for i, d in enumerate(DAYS):
        date = monday + dt.timedelta(days=i)
        for suffix in (d, f"{d}-addon", f"{d}-note"):
            ids[ext(week, suffix)] = date
    ids[ext(week, "checkin")] = monday + dt.timedelta(days=6)
    return ids


# ── commands ─────────────────────────────────────────────────────────────
def cmd_push_week(path, from_date=None, dry_run=False):
    fm, days = parse_week(path)
    events, problems = build_events(fm, days, load_bank())
    if problems:
        sys.exit("Plan problems:\n  " + "\n  ".join(problems))
    week = fm["week"]
    cutoff = dt.date.fromisoformat(from_date) if from_date else None
    if cutoff:
        events = [e for e in events if dt.date.fromisoformat(e["start_date_local"][:10]) >= cutoff]
    keep = {e["external_id"] for e in events}
    stale = [x for x, date in all_ext_ids(week, days[0]["date"]).items()
             if x not in keep and (cutoff is None or date >= cutoff)]
    stale.append(ext(week, "checkin-needed"))
    for e in events:
        print(f"  {e['start_date_local'][:10]}  {e['category']:<7} {e['name']}")
    if dry_run:
        print(f"dry run: {len(events)} to upsert, up to {len(stale)} stale IDs to delete")
        return
    call("PUT", "/events/bulk-delete", [{"external_id": x} for x in stale])
    res = call("POST", "/events/bulk", events, upsert="true")
    errs = [f"{e.get('name')}: {e['push_errors']}" for e in res if e.get("push_errors")]
    print(f"pushed {len(res)} events for {week}")
    if errs:
        print("push errors:\n  " + "\n  ".join(map(str, errs)))


def cmd_clear_week(week):
    y, w = week.split("-W")
    monday = dt.date.fromisocalendar(int(y), int(w), 1)
    ids = list(all_ext_ids(week, monday))
    ids.append(ext(week_id(monday + dt.timedelta(days=7)), "checkin-needed"))
    call("PUT", "/events/bulk-delete", [{"external_id": x} for x in ids])
    print(f"cleared {week}")


def cmd_events(oldest, newest):
    for e in call("GET", "/events", oldest=oldest, newest=newest):
        print(f"{e['start_date_local'][:10]}  {e['category']:<7} {e.get('external_id') or '-':<26} "
              f"{e['name']}" + (f"  [push errors: {e['push_errors']}]" if e.get("push_errors") else ""))


def cmd_rides(oldest, newest):
    acts = call("GET", "/activities", oldest=oldest, newest=newest)
    for a in sorted(acts, key=lambda a: a["start_date_local"]):
        mins = round((a.get("moving_time") or 0) / 60)
        print(f"{a['start_date_local'][:10]}  {a.get('type', ''):<12} {mins:>3} min  "
              f"load {a.get('icu_training_load') or '-':>4}  IF {a.get('icu_intensity') or '-'}  "
              f"HR {a.get('average_heartrate') or '-'}  compliance {a.get('compliance') or '-'}  "
              f"{a.get('name', '')}")
    if not acts:
        print("no activities")


def cmd_fitness(oldest, newest):
    for w in call("GET", "/wellness", oldest=oldest, newest=newest):
        ctl, atl = w.get("ctl"), w.get("atl")
        form = round(ctl - atl, 1) if ctl is not None and atl is not None else "-"
        print(f"{w['id']}  fitness {ctl if ctl is not None else '-':>5}  fatigue {atl if atl is not None else '-':>5}  "
              f"form {form:>5}  ramp {w.get('rampRate', '-')}")


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd, args = argv[1], argv[2:]
    flags = {a for a in args if a == "--dry-run"}
    from_date = None
    if "--from" in args:
        from_date = args[args.index("--from") + 1]
        args = [a for i, a in enumerate(args) if a != "--from" and (i == 0 or args[i - 1] != "--from")]
    args = [a for a in args if a not in flags]
    try:
        if cmd == "push-week":
            cmd_push_week(args[0], from_date, "--dry-run" in flags)
        elif cmd == "clear-week":
            cmd_clear_week(args[0])
        elif cmd in ("events", "rides", "fitness"):
            {"events": cmd_events, "rides": cmd_rides, "fitness": cmd_fitness}[cmd](*args[:2])
        else:
            sys.exit(__doc__)
    except PlanError as e:
        sys.exit(f"Week Record problem: {e}")


if __name__ == "__main__":
    main(sys.argv)
