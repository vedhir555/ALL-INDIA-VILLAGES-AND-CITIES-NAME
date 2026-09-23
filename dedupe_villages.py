#!/usr/bin/env python3
"""
Removes true duplicate rows from the ALL-INDIA-VILLAGES-AND-CITIES-NAME
data: entries that share the same official government village ID
(lgd_code) inside the same district file.

IMPORTANT: this does NOT merge villages that just share a NAME. India has
many distinct villages with the same name in the same taluka - each has
its own lgd_code and its own real coordinates. Merging those would corrupt
the data. This script only touches rows whose lgd_code is IDENTICAL,
which means it's genuinely the same village listed more than once.

Usage:
    python3 dedupe_villages.py /path/to/ALL-INDIA-VILLAGES-AND-CITIES-NAME

What it does per district JSON file ({STATE}/{DISTRICT}.json):
  1. Groups "places" entries by lgd_code.
  2. Rows with no lgd_code are left untouched (can't safely dedupe them).
  3. For a group with more than one row: keeps ONE row, averaging lat/lng
     across the duplicates (they're sometimes very slightly different),
     and keeping the longest/most complete name string.
  4. Rewrites the file only if something changed.
  5. Prints a per-state, then a total, summary of what was removed.

Run it, check the printed summary, then git diff a couple of files to
eyeball the results before committing.
"""
import json
import os
import sys
import glob


def dedupe_file(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    places = data.get("places")
    if not isinstance(places, list):
        return 0, 0  # nothing to do

    groups = {}
    order = []
    passthrough = []  # rows with no lgd_code - never touched
    for p in places:
        code = p.get("lgd_code")
        if code is None:
            passthrough.append(p)
            continue
        if code not in groups:
            groups[code] = []
            order.append(code)
        groups[code].append(p)

    removed = 0
    merged_groups = 0
    new_places = []
    for code in order:
        rows = groups[code]
        if len(rows) == 1:
            new_places.append(rows[0])
            continue
        merged_groups += 1
        removed += len(rows) - 1
        lats = [r["lat"] for r in rows if r.get("lat") is not None]
        lngs = [r["lng"] for r in rows if r.get("lng") is not None]
        best = max(rows, key=lambda r: len(str(r.get("name", ""))))
        merged = dict(best)
        if lats:
            merged["lat"] = sum(lats) / len(lats)
        if lngs:
            merged["lng"] = sum(lngs) / len(lngs)
        new_places.append(merged)

    new_places.extend(passthrough)

    if removed == 0:
        return 0, 0

    data["places"] = new_places
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    return merged_groups, removed


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 dedupe_villages.py /path/to/repo")
        sys.exit(1)

    root = sys.argv[1]
    total_groups = 0
    total_removed = 0
    total_files_changed = 0

    for state_dir in sorted(glob.glob(os.path.join(root, "*/"))):
        state = os.path.basename(state_dir.rstrip("/"))
        state_groups = 0
        state_removed = 0
        state_files_changed = 0
        for fp in glob.glob(os.path.join(state_dir, "*.json")):
            if "index" in os.path.basename(fp).lower():
                continue  # search-index files aren't touched
            try:
                g, r = dedupe_file(fp)
            except Exception as e:
                print(f"  ! skipped {fp}: {e}")
                continue
            if r:
                state_groups += g
                state_removed += r
                state_files_changed += 1
        if state_removed:
            print(f"{state:30s} files_changed={state_files_changed:4d} "
                  f"duplicate_rows_removed={state_removed:5d}")
        total_groups += state_groups
        total_removed += state_removed
        total_files_changed += state_files_changed

    print()
    print(f"TOTAL: {total_files_changed} files changed, "
          f"{total_groups} duplicate groups merged, "
          f"{total_removed} duplicate rows removed.")


if __name__ == "__main__":
    main()
