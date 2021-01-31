from PyQt5.QtWidgets import QApplication
from win32gui import GetForegroundWindow, SetForegroundWindow

from timer_window import TimerWindow


def main():
    app = QApplication([])
    window = TimerWindow()

    temp_hwnd = GetForegroundWindow()
    window.show()
    window.clearFocus()
    SetForegroundWindow(temp_hwnd)

    app.exec_()


if __name__ == "__main__":
    main()
