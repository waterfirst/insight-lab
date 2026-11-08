"""Recompute SP50 counts from the public, pinned typhoon dataset (no API key)."""
import json
import urllib.request
from collections import Counter

COMMIT = "f7e3bccb4ab68810bfe6cfc2568ad5904c3ba69c"
BASE = f"https://raw.githubusercontent.com/waterfirst/Taepoong_trajectory/{COMMIT}/public/data"
BOXES = {"narrow": (32, 40, 124, 132), "standard": (30, 42, 120, 135), "wide": (28, 44, 118, 137)}
counts = Counter()
months = Counter()
for year in range(2020, 2026):
    with urllib.request.urlopen(f"{BASE}/{year}.json", timeout=30) as response:
        data = json.load(response)
    print(year, "tracks", len(data["tracks"]), end="; ")
    annual = Counter()
    for raw in data["tracks"].values():
        points = []
        for line in raw.splitlines():
            row = line.split(",")
            if len(row) < 9 or row[0].strip() != "0":
                continue
            try:
                points.append((row[6].strip(), float(row[7]), float(row[8])))
            except ValueError:
                continue
        points.sort()
        for name, (s, n, w, e) in BOXES.items():
            matches = [p for p in points if s <= p[1] <= n and w <= p[2] <= e]
            if matches:
                counts[name] += 1
                annual[name] += 1
                if name == "standard":
                    months[matches[0][0][4:6]] += 1
    print(dict(annual))
print("Totals:", dict(counts), "first entry months:", dict(months))

