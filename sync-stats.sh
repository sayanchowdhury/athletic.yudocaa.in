#!/usr/bin/env bash
#
# sync-stats.sh — Pull latest weight/waist from daily log entries into stats.yaml
#
# Run after adding or editing a log entry:
#   ./sync-stats.sh
#
# What it does:
#   1. Finds the most recent log entry (by date in frontmatter) that has a weight field
#   2. Updates current_weight and waist_cm in stats.yaml
#   3. Recalculates to_lose and weeks_training
#
set -euo pipefail

STATS_FILE="ath/data/stats.yaml"
LOG_DIR="ath/content/log"

if [ ! -f "$STATS_FILE" ]; then
  echo "Error: $STATS_FILE not found. Run from project root." >&2
  exit 1
fi

# Find the latest log entry with a weight field
# Parse frontmatter from all log .md files, extract date + weight + waist
latest_file=""
latest_date=""
latest_weight=""
latest_waist=""

for f in $(find "$LOG_DIR" -name '*.md' ! -name '_index.md' -type f); do
  # Extract frontmatter (between first two --- lines)
  frontmatter=$(sed -n '/^---$/,/^---$/p' "$f" | sed '1d;$d')

  date_val=$(echo "$frontmatter" | grep -E '^date:' | head -1 | sed 's/^date:[[:space:]]*//' | tr -d '"')
  weight_val=$(echo "$frontmatter" | grep -E '^weight:' | head -1 | sed 's/^weight:[[:space:]]*//' | tr -d '"')

  # Skip entries without weight
  [ -z "$weight_val" ] && continue
  [ -z "$date_val" ] && continue

  # Compare dates (lexicographic works for YYYY-MM-DD)
  if [ -z "$latest_date" ] || [[ "$date_val" > "$latest_date" ]]; then
    latest_date="$date_val"
    latest_weight="$weight_val"
    latest_waist=$(echo "$frontmatter" | grep -E '^waist:' | head -1 | sed 's/^waist:[[:space:]]*//' | tr -d '"')
    latest_file="$f"
  fi
done

if [ -z "$latest_weight" ]; then
  echo "No log entries with weight found."
  exit 0
fi

# Read current values from stats.yaml
old_weight=$(grep '^current_weight:' "$STATS_FILE" | sed 's/^current_weight:[[:space:]]*//')
start_weight=$(grep '^start_weight:' "$STATS_FILE" | sed 's/^start_weight:[[:space:]]*//')
target_weight=$(grep '^target_weight:' "$STATS_FILE" | sed 's/^target_weight:[[:space:]]*//')

# Calculate derived fields
to_lose=$(awk "BEGIN { printf \"%.1f\", $latest_weight - $target_weight }")
# Remove trailing .0
to_lose=$(echo "$to_lose" | sed 's/\.0$//')

# Count weeks since start (first weekly_log date)
first_date=$(grep 'date:' "$STATS_FILE" | head -1 | sed 's/.*date:[[:space:]]*//' | tr -d '"')
if [ -n "$first_date" ]; then
  first_epoch=$(date -d "$first_date" +%s 2>/dev/null || echo "")
  latest_epoch=$(date -d "$latest_date" +%s 2>/dev/null || echo "")
  if [ -n "$first_epoch" ] && [ -n "$latest_epoch" ]; then
    weeks_training=$(( (latest_epoch - first_epoch) / 604800 + 1 ))
  fi
fi

# Update stats.yaml
sed -i "s/^current_weight:.*/current_weight: $latest_weight/" "$STATS_FILE"

if [ -n "$latest_waist" ]; then
  sed -i "s/^waist_cm:.*/waist_cm: $latest_waist/" "$STATS_FILE"
fi

sed -i "s/^to_lose:.*/to_lose: \"~$to_lose\"/" "$STATS_FILE"

if [ -n "${weeks_training:-}" ]; then
  sed -i "s/^weeks_training:.*/weeks_training: $weeks_training/" "$STATS_FILE"
fi

echo "Updated stats.yaml from $latest_file ($latest_date)"
echo "  weight: $old_weight → $latest_weight"
[ -n "$latest_waist" ] && echo "  waist:  → $latest_waist"
echo "  to_lose: ~$to_lose kg"
[ -n "${weeks_training:-}" ] && echo "  weeks_training: $weeks_training"
