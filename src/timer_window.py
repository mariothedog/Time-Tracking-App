from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel


class TimerWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Window Timer")
        self.setFixedSize(100, 30)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("border:1px solid black")
        self.setFocusPolicy(Qt.NoFocus)

        self.label = QLabel("0:00:00")
        self.label.setFont(QFont("MS Shell Dlg 2", 16))
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

    def closeEvent(self, event):
        event.ignore()
