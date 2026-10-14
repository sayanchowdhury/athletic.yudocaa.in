#!/usr/bin/env python3
"""Summarise Garmin .FIT activities into ath/data/activities.json.

Drop .fit files, or the .zip files Garmin Connect exports, into scripts/fit/.
Only summary fields are kept (no GPS, no heart rate). Existing entries are preserved and new
files are merged in by id, so CI can build without the raw files.
Needs `fitdecode` only when there are new files to read.
"""

import io
import json
import zipfile
from datetime import timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "fit"
OUT = ROOT / "ath" / "data" / "activities.json"
IST = timezone(timedelta(hours=5, minutes=30))
TYPES = {"running": "run", "walking": "walk"}


def clock(seconds):
    s = round(seconds)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def sources():
    """Yield (id, bytes) for every .fit, including those inside .zip files."""
    for p in sorted(SRC.glob("*")):
        if p.suffix.lower() == ".fit":
            yield p.stem, p.read_bytes()
        elif p.suffix.lower() == ".zip":
            with zipfile.ZipFile(p) as z:
                for name in z.namelist():
                    if name.lower().endswith(".fit"):
                        yield Path(name).stem, z.read(name)


def summarise(fid, data, fitdecode):
    with fitdecode.FitReader(io.BytesIO(data)) as reader:
        for frame in reader:
            if frame.frame_type != fitdecode.FIT_FRAME_DATA or frame.name != "session":
                continue
            f = {x.name: x.value for x in frame.fields}
            start = f["start_time"].astimezone(IST)
            sport = f.get("sport", "other")
            out = {
                "id": fid,
                "date": start.strftime("%Y-%m-%d"),
                "start": start.strftime("%H:%M"),
                "type": TYPES.get(sport, sport),
                "distance_km": round(f.get("total_distance", 0) / 1000, 2),
                "moving_time": clock(f.get("total_timer_time", 0)),
            }
            return out
    return None


def main():
    existing = json.loads(OUT.read_text()) if OUT.exists() else []
    known = {a["id"] for a in existing}
    files = [(i, d) for i, d in sources() if i not in known] if SRC.is_dir() else []
    if not files:
        print("activities: nothing new")
        return
    import fitdecode

    added = 0
    for fid, data in files:
        entry = summarise(fid, data, fitdecode)
        if entry:
            existing.append(entry)
            added += 1
    existing.sort(key=lambda a: (a["date"], a["start"]))
    OUT.write_text(json.dumps(existing, indent=2) + "\n")
    print(f"activities: added {added}, total {len(existing)}")


if __name__ == "__main__":
    main()
