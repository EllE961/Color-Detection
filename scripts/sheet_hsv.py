"""Median HSV of each sheet in docs/assets/paper.jpg and the color names that match it.

    python scripts/sheet_hsv.py
"""
import json
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_figures import ROOT, load_ranges  # noqa: E402

# x1, y1, x2, y2 inside each sheet of the 800x599 photo
SHEETS = {"cream": (200, 70, 300, 130), "blue": (420, 60, 560, 130), "green": (150, 200, 330, 320),
          "brick red": (400, 190, 600, 300), "dark purple": (120, 370, 330, 520), "yellow": (420, 360, 650, 510),
          "carpet": (20, 560, 120, 590)}


def main():
    ranges = load_ranges()
    hsv = cv2.cvtColor(cv2.imread(os.path.join(ROOT, "docs", "assets", "paper.jpg")), cv2.COLOR_BGR2HSV)
    out = {}
    for name, (x1, y1, x2, y2) in SHEETS.items():
        h, s, v = (int(x) for x in np.median(hsv[y1:y2, x1:x2].reshape(-1, 3), axis=0))
        names = [n for n, rs in ranges.items()
                 if any(all(lo[i] <= x <= hi[i] for i, x in enumerate((h, s, v))) for lo, hi in rs)]
        out[name] = {"median_hsv": [h, s, v], "names_matching_median": names}
        print(f"{name:12s} H {h:3d}  S {s:3d}  V {v:3d}  {', '.join(names) or '(none)'}")
    with open(os.path.join(ROOT, "results", "paper_sheets.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
