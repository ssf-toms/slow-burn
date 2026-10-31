#!/usr/bin/env python3
"""intervals.icu client for slow-burn.

Usage:
  icu.py push-week athlete/weeks/2026-W44.md [--from YYYY-MM-DD] [--dry-run]
  icu.py clear-week 2026-W44
  icu.py events  YYYY-MM-DD YYYY-MM-DD
  icu.py rides   YYYY-MM-DD YYYY-MM-DD
  icu.py fitness YYYY-MM-DD YYYY-MM-DD
  icu.py whoami                  name and ID the API key belongs to, checked against .env
  icu.py test-ride YYYY-MM-DD    push a short Setup test ride; prints its event ID
  icu.py delete-event EVENT_ID

Week Record format: docs/week-records.md. Workout Bank: bank/README.md.
push-week checks the plan against the Athlete Profile (docs/athlete-profile.md),
read from athlete/profile.md, or $ATHLETE_DIR/profile.md when that is set.
Credentials: INTERVALS_ATHLETE_ID and INTERVALS_KEYCHAIN_SERVICE in .env, API
key in the macOS Keychain. The /setup skill sets all three up.
"""
import base64
import datetime as dt
import inspect
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://intervals.icu/api/v1"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SESSION_KINDS = {"Recovery", "Quality", "Endurance", "Test", "Strength", "Other"}
OTHER = "other:"                # Workout cell prefix for the profile's `other` activities
SMART_TRAINER = "smart-trainer"  # equipment tag
EXTENSION_MIN = (10, 15)         # allowed Extension minutes, Push Quality rides only
EXTENSION_PCT = 68               # Endurance (Zone 2) %FTP for Extension minutes
ROUNDS = {"light": 2, "normal": 3, "push": 4}  # composed strength, by Week Level
STRENGTH_BLOCK = (3, 8)          # Exercises in a Workout cell's composed block
ADD_ON_BLOCK = (2, 4)            # Exercises in an Add-on
PACES = ("easy_run_pace", "threshold_run_pace")  # profile fields run Workouts write as {field}


class PlanError(Exception):
    pass


class ProfileError(PlanError):
    pass


# ── config and HTTP ──────────────────────────────────────────────────────
def load_env():
    env, path = {}, ROOT / ".env"
    if not path.exists():  # dry runs and tests need no credentials
        return env
    for line in path.read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")
    return env


ENV = load_env()
ATHLETE = ENV.get("INTERVALS_ATHLETE_ID")


def api_key():
    return subprocess.run(
        ["security", "find-generic-password", "-a", subprocess.getoutput("id -un"),
         "-s", ENV["INTERVALS_KEYCHAIN_SERVICE"], "-w"],
        check=True, capture_output=True, text=True).stdout.strip()


def call(method, path, body=None, athlete_id=None, /, **query):
    """`path` is under /athlete/<id>; athlete_id "0" means whoever owns the key.
    The first four are positional-only, so every keyword is a query param."""
    url = f"{API}/athlete/{athlete_id or ATHLETE}{path}"
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
def split_top(s):
    """Split on commas outside quotes, brackets and braces."""
    parts, depth, quoted, cur = [], 0, False, ""
    for ch in s:
        if ch == '"':
            quoted = not quoted
        elif not quoted and ch in "[{":
            depth += 1
        elif not quoted and ch in "]}":
            depth -= 1
        if ch == "," and depth == 0 and not quoted:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def parse_value(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [parse_value(x) for x in split_top(v[1:-1])]
    if v.startswith("{") and v.endswith("}"):
        return {k.strip(): parse_value(x) for k, _, x in
                (item.partition(":") for item in split_top(v[1:-1]))}
    if len(v) >= 2 and v[0] == v[-1] == '"':
        return v[1:-1].replace('\\"', '"')
    return v


def parse_block(lines, i=0, indent=0):
    """The YAML subset in docs/athlete-profile.md: maps nested by indentation,
    `- item` lists, and inline [..] / {..} values. Scalars stay strings."""
    out = {}
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        depth = len(line) - len(line.lstrip(" "))
        if depth < indent:
            break
        key, _, v = line.strip().partition(":")
        key = key.strip()
        i += 1
        if v.strip():
            out[key] = parse_value(v)
            continue
        nxt = next((l for l in lines[i:] if l.strip()), "")
        child = len(nxt) - len(nxt.lstrip(" "))
        if child <= depth:
            out[key] = ""
        elif nxt.lstrip().startswith("- "):
            items = []
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                items.append(parse_value(lines[i].lstrip()[2:]))
                i += 1
            out[key] = items
        else:
            out[key], i = parse_block(lines, i, child)
    return out, i


def split_frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise PlanError("missing frontmatter")
    return parse_block(m.group(1).splitlines())[0], m.group(2)


def athlete_dir():
    return Path(os.environ.get("ATHLETE_DIR") or ROOT / "athlete")


def load_profile():
    path = athlete_dir() / "profile.md"
    if not path.exists():
        raise ProfileError(f"no Athlete Profile at {path}: run /setup")
    return split_frontmatter(path.read_text())[0]


def load_exercise(fm, body):
    """An Exercise (bank/exercises/, ADR 0004): pushed only inside a composed note."""
    cue = re.sub(r"\n?Progress:.*", "", body.strip(), flags=re.S).strip()
    return {**fm, "kind": "exercise", "sport": "strength", "delivery": "note",
            "cue": " ".join(cue.split()), "prose": body.strip()}


def load_bank(bank_dir=None):
    """Workouts and Exercises, keyed by ID in one namespace."""
    bank, where = {}, {}
    bank_dir = Path(bank_dir or ROOT / "bank")
    for p in sorted(bank_dir.rglob("*.md")):
        if p.name == "README.md":
            continue
        fm, body = split_frontmatter(p.read_text())
        if fm["id"] in bank:
            raise PlanError(f"duplicate Bank ID {fm['id']}: {where[fm['id']]} and {p}")
        where[fm["id"]] = p
        if p.parent.name == "exercises":
            bank[fm["id"]] = load_exercise(fm, body)
            continue
        block = re.search(r"```intervals\n(.*?)\n```", body, re.S)
        prose = re.sub(r"```intervals\n.*?\n```", "", body, flags=re.S)
        prose = re.sub(r"^# .*\n", "", prose.strip())
        prose = re.sub(r"\n?Alternative: swap this for .*", "", prose).strip()
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
        ids, extend = [], None
        for token in (w.strip() for w in workouts.split(",") if w.strip()):
            m = re.fullmatch(r"(\S+?)\s*\+(\d+)", token)
            if m:
                if extend is not None:
                    raise PlanError(f"{day}: more than one Extension")
                token, extend = m.group(1), (m.group(1), int(m.group(2)))
            ids.append(token)
        days.append(dict(day=day, date=date, session=session, workouts=ids,
                         addon=split_top(addon), extend=extend))
    if [d["day"] for d in days] != DAYS:
        raise PlanError("Plan must list Mon..Sun once each, in order")
    return fm, days


# ── building events ──────────────────────────────────────────────────────
def week_id(date):
    y, w, _ = date.isocalendar()
    return f"{y}-W{w:02d}"


def ext(week, suffix):
    return f"tp-{week}-{suffix}"


def other_workouts(profile):
    """The profile's `other` activities as note Workouts, keyed `other:<id>`."""
    return {OTHER + o["id"]: dict(id=OTHER + o["id"], name=o["name"], sport="other",
                                  delivery="note", equipment=[],
                                  prose=f"{o['name']}, {o['minutes']} min.")
            for o in profile.get("other") or []}


def needed_equipment(w):
    # A smart trainer only decides whether a structured ride is indoor or outdoor.
    return [t for t in w.get("equipment") or []
            if not (t == SMART_TRAINER and w["delivery"] == "workout")]


def alternatives_of(w):
    """A Workout's `alternative`, one ID or a list in order of preference."""
    alt = w.get("alternative") or []
    return [alt] if isinstance(alt, str) else alt


def note_event(name, description, date, external_id):
    when = f"{date}T00:00:00"
    return dict(category="NOTE", name=name, description=description,
                start_date_local=when, end_date_local=when, external_id=external_id)


def row_ids(d):
    return d["workouts"] + d["addon"]


def is_exercise(w):
    return w.get("kind") == "exercise"


def grouped(ids, bank):
    """A cell's Workouts in order, with each run of consecutive Exercises as one list."""
    out = []
    for w in (bank[i] for i in ids):
        if not is_exercise(w):
            out.append(w)
        elif out and isinstance(out[-1], list):
            out[-1].append(w)
        else:
            out.append([w])
    return out


def composed_note(label, exercises, level):
    """One composed block as a note Workout: rounds from the Level (ADR 0004)."""
    rounds = ROUNDS.get(level, ROUNDS["normal"])
    lines = [f"- {e['name']} × {e.get('reps') or e.get('hold')}: {e['cue']}" for e in exercises]
    return dict(id="+".join(e["id"] for e in exercises), name=f"{label} ({rounds} rounds)",
                sport="strength", delivery="note", equipment=[],
                prose=f"{rounds} rounds, resting 60–90 s between rounds.\n\n" + "\n".join(lines))


def composed(ids, bank, label, level):
    """A cell's Workouts, with each block of Exercises composed into one note."""
    return [composed_note(label, g, level) if isinstance(g, list) else g
            for g in grouped(ids, bank)]


def pairing_problem(session, workouts, pairings):
    if session == "Test" or len(workouts) < 2:
        return None  # a Test row is the test note plus its spin, not a pairing
    if session == "Quality":
        return "nothing can be paired with a Quality Session"
    if any(w["sport"] == "other" for w in workouts):
        return "other activities can't be paired"
    sports = [w["sport"] for w in workouts]
    if not any(set(p.split("+")) == set(sports) for p in pairings):
        return (f"{' + '.join(sports)} is not an allowed pairing "
                f"(profile pairings: {', '.join(pairings) or 'none'})")
    return None


def plan_problems(d, bank, level, profile):
    """What's wrong with one Plan row. `bank` includes the profile's other activities."""
    equipment = set(profile.get("equipment") or [])
    problems = []
    if d["session"] not in SESSION_KINDS:
        problems.append(f"unknown Session '{d['session']}'")
    if d["addon"] and d["session"] not in ("Endurance", "Test"):
        problems.append("Add-on only allowed on Endurance or Test rows")
    ids = row_ids(d)
    unknown_other = [w for w in ids if w.startswith(OTHER) and w not in bank]
    for w in unknown_other:
        problems.append(f"{w} is not in the profile's other activities")
    missing = [w for w in ids if w not in bank and w not in unknown_other]
    if missing:
        problems.append(f"not in Bank: {', '.join(missing)}")
    if missing or unknown_other:
        return problems
    for w in (bank[i] for i in d["workouts"]):
        if w.get("levels") and level not in w["levels"]:
            problems.append(f"{w['id']} is for {'/'.join(w['levels'])} weeks only")
    for w in [bank[i] for i in ids]:
        lacking = [t for t in needed_equipment(w) if t not in equipment]
        if lacking:
            problems.append(f"{w['id']} needs {', '.join(lacking)} (not in the profile's equipment)")
        for pace in PACES:
            if "{" + pace + "}" in w["prose"] and not profile.get(pace):
                problems.append(f"{w['id']} needs {pace} in the profile")
    problems += composition_problems(d, bank)
    workouts = composed(d["workouts"], bank, "Strength", level)
    pairing = pairing_problem(d["session"], workouts, profile.get("pairings") or [])
    if pairing:
        problems.append(pairing)
    if sum(w["delivery"] == "workout" for w in workouts) > 1:
        problems.append("more than one ride Workout")
    if d.get("extend"):
        problems += extension_problems(d, bank, level)
    return problems


def composition_problems(d, bank):
    """Composed strength: block sizes, no repeats, Exercise-only Add-ons (ADR 0004)."""
    problems = []
    blocks = [g for g in grouped(d["workouts"], bank) if isinstance(g, list)]
    if len(blocks) > 1:
        problems.append("a Workout cell has one block of consecutive Exercises")
    for b in blocks:
        if not STRENGTH_BLOCK[0] <= len(b) <= STRENGTH_BLOCK[1]:
            problems.append(f"a Strength block needs {STRENGTH_BLOCK[0]}–{STRENGTH_BLOCK[1]} "
                            f"Exercises, has {len(b)}")
    not_exercises = [i for i in d["addon"] if not is_exercise(bank[i])]
    if not_exercises:
        problems.append(f"the Add-on holds Exercises only, not {', '.join(not_exercises)}")
    elif d["addon"] and not ADD_ON_BLOCK[0] <= len(d["addon"]) <= ADD_ON_BLOCK[1]:
        problems.append(f"an Add-on needs {ADD_ON_BLOCK[0]}–{ADD_ON_BLOCK[1]} "
                        f"Exercises, has {len(d['addon'])}")
    exercise_ids = [i for i in row_ids(d) if is_exercise(bank[i])]
    for i in dict.fromkeys(i for i in exercise_ids if exercise_ids.count(i) > 1):
        problems.append(f"{i} is in the row twice")
    return problems


def extension_problems(d, bank, level):
    wid, minutes = d["extend"]
    lo, hi = EXTENSION_MIN
    problems = []
    if level != "push":
        problems.append(f"{wid} +{minutes}: Extensions are for Push weeks only")
    if d["session"] != "Quality" or bank[wid]["delivery"] != "workout":
        problems.append(f"{wid} +{minutes}: only a Quality ride can have an Extension")
    if not lo <= minutes <= hi:
        problems.append(f"{wid} +{minutes}: an Extension is {lo}–{hi} min")
    return problems


def extended(workout_text, minutes):
    """Insert `minutes` at Endurance before the Cooldown section."""
    block = f"Extension\n- {minutes}m {EXTENSION_PCT}%\n\n"
    if "\nCooldown" not in workout_text:
        return workout_text.rstrip() + "\n\n" + block.rstrip()
    return workout_text.replace("\nCooldown", "\n" + block + "Cooldown", 1)


def build_events(fm, days, bank, profile):
    week, level = fm["week"], fm["level"]
    bank = {**bank, **other_workouts(profile)}
    equipment = set(profile.get("equipment") or [])
    tiered = set(profile.get("tiers") or {})
    indoor = SMART_TRAINER in equipment
    alternatives = profile.get("alternatives") == "on"

    def description(w):
        out = w["prose"]
        for pace in PACES:
            out = out.replace("{" + pace + "}", profile.get(pace) or "{" + pace + "}")
        dose = (w.get("dose") or {}).get(level)
        return out + (f"\n\nToday: {dose}" if dose else "")

    def offered(alt):
        return (alternatives and alt is not None and alt["sport"] in tiered
                and all(t in equipment for t in needed_equipment(alt)))

    def alternative_line(w):
        """The first of the Workout's Alternatives the profile can use, if any."""
        alt = next((bank[a] for a in alternatives_of(w) if offered(bank.get(a))), None)
        return f"\n\nAlternative: {alt['name']}. {description(alt)}" if alt else ""

    def combined(workouts):
        return (" + ".join(w["name"] for w in workouts),
                "\n\n".join(description(w) + alternative_line(w) for w in workouts))

    events, problems = [], []
    if sum(1 for d in days if d.get("extend")) > 1:
        problems.append("at most one Extension a week")
    for d in days:
        if not d["session"] and not d["workouts"] and not d["addon"]:
            continue  # unplanned day in a partial week
        problems += [f"{d['day']}: {p}" for p in plan_problems(d, bank, level, profile)]
        if any(w not in bank for w in row_ids(d)):
            continue
        workouts = composed(d["workouts"], bank, "Strength", level)
        rides = [w for w in workouts if w["delivery"] == "workout"]
        notes = [w for w in workouts if w["delivery"] != "workout"]
        if rides and notes:  # e.g. Test row: MyWhoosh test note + pushed spin
            events.append(note_event(*combined(notes), d["date"], ext(week, f"{d['day']}-note")))
        if rides:
            ride = rides[0]
            name, text = ride["name"], ride["workout_text"]
            desc = description(ride)
            if d.get("extend") and d["extend"][0] == ride["id"]:
                minutes = d["extend"][1]
                name += f" +{minutes}′"
                text = extended(text, minutes)
                desc += f"\n\nToday: +{minutes} min at Endurance ({EXTENSION_PCT}%) before the cooldown."
            desc += alternative_line(ride)
            desc += "\n\n" + text
            events.append(dict(category="WORKOUT", type="Ride", indoor=indoor, name=name,
                               description=desc, start_date_local=f"{d['date']}T00:00:00",
                               external_id=ext(week, d["day"])))
        elif workouts:
            events.append(note_event(*combined(workouts), d["date"], ext(week, d["day"])))
        if d["addon"] and all(is_exercise(bank[i]) for i in d["addon"]):
            addon = composed_note("Add-on", [bank[i] for i in d["addon"]], level)
            events.append(note_event(addon["name"], description(addon), d["date"],
                                     ext(week, f"{d['day']}-addon")))
    sunday = days[-1]["date"]
    monday = sunday + dt.timedelta(days=1)
    events.append(note_event("Check-in: plan next week",
                             "Sunday Check-in with Claude: review this week, pick next week's Level.",
                             sunday, ext(week, "checkin")))
    events.append(note_event("Check-in needed",
                             "No Week Plan yet for this week. Run the Check-in with Claude.",
                             monday, ext(week_id(monday), "checkin-needed")))
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
    events, problems = build_events(fm, days, load_bank(), load_profile())
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


def cmd_whoami():
    if not ATHLETE:
        sys.exit("INTERVALS_ATHLETE_ID isn't set in .env")
    me = call("GET", "", None, "0")
    print(f"authenticated as {me.get('name') or '?'} ({me['id']})")
    if me["id"] != ATHLETE:
        sys.exit(f"API says your athlete ID is {me['id']}, not {ATHLETE} as in .env")


TEST_RIDE = "- 10m 55%\n\n3x\n- 2m 75%\n- 2m 55%\n\n- 5m 50%"


def cmd_test_ride(date):
    when = f"{dt.date.fromisoformat(date)}T00:00:00"
    ev = call("POST", "/events", dict(category="WORKOUT", type="Ride", name="Setup test (delete me)",
                                      start_date_local=when, description=TEST_RIDE))
    print(ev["id"])


def cmd_delete_event(event_id):
    call("DELETE", f"/events/{event_id}")
    print(f"deleted event {event_id}")


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
    commands = {
        "push-week": lambda path: cmd_push_week(path, from_date, "--dry-run" in flags),
        "clear-week": cmd_clear_week,
        "events": cmd_events,
        "rides": cmd_rides,
        "fitness": cmd_fitness,
        "whoami": cmd_whoami,
        "test-ride": cmd_test_ride,
        "delete-event": cmd_delete_event,
    }
    if cmd not in commands:
        sys.exit(__doc__)
    try:
        inspect.signature(commands[cmd]).bind(*args)
    except TypeError:
        sys.exit(__doc__)
    try:
        commands[cmd](*args)
    except ProfileError as e:
        sys.exit(f"Athlete Profile problem: {e}")
    except PlanError as e:
        sys.exit(f"Week Record problem: {e}")


if __name__ == "__main__":
    main(sys.argv)
