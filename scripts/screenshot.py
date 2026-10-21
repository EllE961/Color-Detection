"""Run the app on a still image instead of the webcam and save a screenshot of the window.

cv2.VideoCapture is swapped for a class that returns the image every time, the window is
created with Qt.WA_DontShowOnScreen so nothing appears on the desktop, update_frame() runs
once, and QWidget.grab() saves what the window shows. The label of every box the app draws
is counted, and update_frame() is then timed over 20 more calls.

    python scripts/screenshot.py docs/assets/balloons.jpg docs/assets/app_balloons.png
"""
import json
import os
import sys
import time
from collections import Counter

import cv2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
image_path, out_path = sys.argv[1], sys.argv[2]


class StillCapture:
    def __init__(self, *_):
        self.frame = cv2.imread(image_path)

    def isOpened(self):
        return self.frame is not None

    def read(self):
        return True, self.frame.copy()

    def release(self):
        pass


cv2.VideoCapture = StillCapture
labels = Counter()
_put_text = cv2.putText


def counting_put_text(img, text, *args, **kwargs):
    labels[text] += 1
    return _put_text(img, text, *args, **kwargs)


cv2.putText = counting_put_text

from PyQt5.QtCore import Qt  # noqa: E402
from PyQt5.QtWidgets import QApplication  # noqa: E402

import color_detection_app as app  # noqa: E402

qt = QApplication(sys.argv)
window = app.ExpandedColorDetectionApp()
window.timer.stop()
window.setAttribute(Qt.WA_DontShowOnScreen)
window.update_frame()
window.show()
qt.processEvents()
window.grab().save(out_path)
counts = dict(labels.most_common())
cv2.putText = _put_text
times = []
for _ in range(20):
    t = time.perf_counter()
    window.update_frame()
    times.append(time.perf_counter() - t)
times.sort()
h, w = window.cap.frame.shape[:2]
print(json.dumps({"image": os.path.basename(image_path), "size": [w, h], "boxes": sum(counts.values()),
                  "names_drawn": len(counts), "update_frame_ms_median": round(times[10] * 1000, 1),
                  "per_name": counts}, indent=1))
