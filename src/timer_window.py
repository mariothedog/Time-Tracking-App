from datetime import timedelta

import psutil

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel

from win32gui import GetForegroundWindow, SetForegroundWindow, GetWindowText, GetWindowRect
from win32process import GetWindowThreadProcessId


class TimerWindow(QMainWindow):
    INTERVAL_UPDATE_WINDOW = 1000
    WINDOW_PADDING_X_RIGHT = 30

    seconds_spent = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Window Timer")
        self.setFixedSize(100, 30)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("border:1px solid black")

        self.label = QLabel("0:00:00")
        self.label.setFont(QFont("MS Shell Dlg 2", 16))
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        self.update_window()

        self.update_window_timer = QTimer(self)
        self.update_window_timer.timeout.connect(self.update_window)
        self.update_window_timer.start(self.INTERVAL_UPDATE_WINDOW)

    def closeEvent(self, event):
        event.ignore()

    def update_window(self):
        hwnd = GetForegroundWindow()
        name = None
        if hwnd:
            if GetWindowText(hwnd) == self.windowTitle():  # Prevent focus on timer window
                SetForegroundWindow(self.last_hwnd)
                hwnd = self.last_hwnd

            rect = GetWindowRect(hwnd)
            pos_x = rect[2] - self.width() - self.WINDOW_PADDING_X_RIGHT
            pos_y = rect[1] + self.height()
            self.move(pos_x, pos_y)

            pid = GetWindowThreadProcessId(hwnd)[1]
            process = psutil.Process(pid)

            name = process.name()
            if name in self.seconds_spent:
                self.seconds_spent[name] += 1
            else:
                self.seconds_spent[name] = 0
            seconds = self.seconds_spent[name]
            self.label.setText(str(timedelta(seconds=seconds)))

        self.last_hwnd = hwnd
