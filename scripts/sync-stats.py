#!/usr/bin/env python3
"""Parse the 2026 journal and update stats.yaml with current weight + weekly log."""

import re
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOURNAL = ROOT / "ath" / "content" / "log" / "2026" / "journal.md"
STATS = ROOT / "ath" / "data" / "stats.yaml"

START_DATE = datetime(2026, 3, 2)  # Monday (first journal entry)


def parse_journal(path):
    """Return list of (date, weight) sorted ascending by date."""
    text = path.read_text()
    entries = []
    current_date = None
    for line in text.splitlines():
        m = re.match(r"### (\w+ \d{1,2}, \d{4})", line)
        if m:
            current_date = datetime.strptime(m.group(1), "%B %d, %Y")
            continue
        if current_date:
            m = re.match(r"cw:\s*([\d.]+)", line)
            if m:
                entries.append((current_date, float(m.group(1))))
                current_date = None
    entries.sort(key=lambda x: x[0])
    return entries


def build_weekly_log(entries):
    """Group entries by week (Sun-Sat) and pick the last weight per week."""
    if not entries:
        return []

    # Build date->weight map
    by_date = {d.date(): w for d, w in entries}

    # Find week boundaries (Monday-based)
    last = max(d for d, _ in entries).date()

    weeks = []
    week_start = START_DATE.date()
    week_num = 1
    prev_weight = None

    while week_start <= last:
        week_start_date = week_start

        # Find first logged weight in this week (Monday weigh-in)
        weight = None
        for d in range(7):
            day = week_start_date + timedelta(days=d)
            if day in by_date:
                weight = by_date[day]
                break

        if weight is not None:
            change = round(weight - prev_weight, 2) if prev_weight is not None else 0.0
            weeks.append({
                "week": week_num,
                "date": week_start_date.isoformat(),
                "weight": weight,
                "change": change,
            })
            prev_weight = weight

        week_num += 1
        week_start += timedelta(days=7)

    return weeks


def update_stats(entries, weekly_log):
    """Rewrite stats.yaml with latest weight and weekly log."""
    latest_weight = entries[-1][1]
    text = STATS.read_text()

    # Update current_weight
    text = re.sub(r"^current_weight:.*$", f"current_weight: {latest_weight}", text, flags=re.M)

    # Update to_lose
    target_m = re.search(r"^target_weight:\s*([\d.]+)", text, re.M)
    if target_m:
        to_lose = round(latest_weight - float(target_m.group(1)), 1)
        text = re.sub(r'^to_lose:.*$', f'to_lose: "~{to_lose}"', text, flags=re.M)

    # Replace weekly_log section (everything from "weekly_log:" to end of file)
    weekly_yaml = "weekly_log:\n"
    for w in weekly_log:
        weekly_yaml += f"  - week: {w['week']}\n"
        weekly_yaml += f'    date: "{w["date"]}"\n'
        weekly_yaml += f"    weight: {w['weight']}\n"
        change = w["change"]
        weekly_yaml += f"    change: {change}\n"

    text = re.sub(r"^# Weekly weigh-in log.*", "", text, flags=re.M)
    text = re.sub(r"^weekly_log:.*", "", text, flags=re.M | re.S)
    text = text.rstrip() + "\n\n" + weekly_yaml

    STATS.write_text(text)
    print(f"Updated current_weight to {latest_weight}")
    print(f"Updated weekly_log with {len(weekly_log)} weeks")


def main():
    entries = parse_journal(JOURNAL)
    if not entries:
        print("No entries found in journal")
        return
    weekly_log = build_weekly_log(entries)
    update_stats(entries, weekly_log)


if __name__ == "__main__":
    main()
