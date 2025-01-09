import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QVBoxLayout, QPushButton
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class ExpandedColorDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Colors Detection")

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam.")

        self.color_ranges = {
            "Red": [
                (np.array([0, 120, 70]), np.array([10, 255, 255])),
                (np.array([170, 120, 70]), np.array([180, 255, 255]))
            ],
            "DarkRed": [
                (np.array([170, 100, 50]), np.array([180, 255, 120]))
            ],
            "Crimson": [
                (np.array([170, 150, 100]), np.array([180, 255, 170]))
            ],
            "Coral": [
                (np.array([5, 100, 100]), np.array([15, 255, 255]))
            ],
            "Salmon": [
                (np.array([5, 80, 150]), np.array([15, 170, 255]))
            ],
            "Pink": [
                (np.array([150, 100, 100]), np.array([170, 255, 255]))
            ],
            "HotPink": [
                (np.array([160, 120, 120]), np.array([170, 255, 255]))
            ],
            "Magenta": [
                (np.array([145, 100, 100]), np.array([160, 255, 255]))
            ],
            "Fuchsia": [
                (np.array([150, 150, 150]), np.array([165, 255, 255]))
            ],
            "Maroon": [
                (np.array([170, 100, 50]), np.array([180, 200, 150]))
            ],
            "Brown": [
                (np.array([10, 40, 40]), np.array([20, 200, 150]))
            ],
            "SaddleBrown": [
                (np.array([10, 60, 50]), np.array([20, 180, 120]))
            ],
            "Chocolate": [
                (np.array([10, 60, 40]), np.array([20, 200, 120]))
            ],
            "Orange": [
                (np.array([10, 150, 100]), np.array([25, 255, 255]))
            ],
            "DarkOrange": [
                (np.array([10, 150, 100]), np.array([20, 255, 255]))
            ],
            "Gold": [
                (np.array([20, 150, 100]), np.array([30, 255, 255]))
            ],
            "Yellow": [
                (np.array([25, 150, 100]), np.array([35, 255, 255]))
            ],
            "LightYellow": [
                (np.array([25, 50, 150]), np.array([35, 120, 255]))
            ],
            "Khaki": [
                (np.array([25, 50, 90]), np.array([35, 120, 140]))
            ],
            "Green": [
                (np.array([36, 100, 100]), np.array([70, 255, 255]))
            ],
            "LightGreen": [
                (np.array([40, 60, 120]), np.array([70, 255, 255]))
            ],
            "DarkGreen": [
                (np.array([36, 120, 50]), np.array([70, 255, 100]))
            ],
            "Lime": [
                (np.array([35, 150, 100]), np.array([50, 255, 255]))
            ],
            "Olive": [
                (np.array([40, 80, 40]), np.array([65, 150, 120]))
            ],
            "Teal": [
                (np.array([85, 100, 100]), np.array([95, 255, 255]))
            ],
            "Cyan": [
                (np.array([85, 150, 100]), np.array([95, 255, 255]))
            ],
            "Aqua": [
                (np.array([80, 100, 100]), np.array([90, 255, 255]))
            ],
            "Turquoise": [
                (np.array([80, 120, 120]), np.array([95, 255, 255]))
            ],
            "Blue": [
                (np.array([95, 100, 100]), np.array([125, 255, 255]))
            ],
            "LightBlue": [
                (np.array([90, 70, 120]), np.array([110, 200, 255]))
            ],
            "DarkBlue": [
                (np.array([90, 150, 50]), np.array([120, 255, 100]))
            ],
            "Navy": [
                (np.array([100, 150, 50]), np.array([120, 255, 80]))
            ],
            "Indigo": [
                (np.array([126, 100, 100]), np.array([135, 255, 255]))
            ],
            "Purple": [
                (np.array([136, 100, 100]), np.array([150, 255, 255]))
            ],
            "DarkPurple": [
                (np.array([140, 150, 50]), np.array([160, 255, 120]))
            ],
            "Violet": [
                (np.array([140, 100, 120]), np.array([160, 255, 255]))
            ],
            "Plum": [
                (np.array([135, 30, 80]), np.array([155, 60, 180]))
            ],
            "Lavender": [
                (np.array([130, 50, 150]), np.array([140, 150, 255]))
            ],
            "PinkPurple": [
                (np.array([150, 70, 100]), np.array([165, 255, 255]))
            ],
            "Gray": [
                (np.array([0, 0, 40]), np.array([180, 30, 200]))
            ],
            "DarkGray": [
                (np.array([0, 0, 20]), np.array([180, 30, 120]))
            ],
            "Silver": [
                (np.array([0, 0, 100]), np.array([180, 20, 220]))
            ],
            "Beige": [
                (np.array([15, 10, 200]), np.array([30, 60, 255]))
            ],
            "SkyBlue": [
                (np.array([90, 70, 120]), np.array([110, 200, 255]))
            ],
            "Khaki": [
                (np.array([25, 50, 90]), np.array([35, 120, 140]))
            ],
            "Salmon": [
                (np.array([5, 80, 150]), np.array([15, 170, 255]))
            ],
            "Coral": [
                (np.array([5, 100, 100]), np.array([15, 255, 255]))
            ],
            "Chocolate": [
                (np.array([10, 60, 40]), np.array([20, 200, 120]))
            ],
            "Maroon": [
                (np.array([170, 100, 50]), np.array([180, 200, 150]))
            ]
        }

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.video_label = QLabel("Camera Feed")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_app)
        self.layout.addWidget(self.close_button)

        self.central_widget.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        overlay = frame.copy()

        for color_name, hsv_ranges in self.color_ranges.items():
            full_mask = None
            for (lower, upper) in hsv_ranges:
                mask = cv2.inRange(hsv, lower, upper)
                full_mask = mask if full_mask is None else cv2.bitwise_or(full_mask, mask)

            # Find contours
            contours, _ = cv2.findContours(full_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 500:  # skip small noise
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    cv2.putText(overlay, color_name, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        hh, ww, ch = rgb.shape
        bytes_per_line = ch * ww
        qt_img = QImage(rgb.data, ww, hh, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qt_img)
        self.video_label.setPixmap(pix)

    def close_app(self):
        self.timer.stop()
        self.cap.release()
        self.close()

def main():
    app = QApplication(sys.argv)
    window = ExpandedColorDetectionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
