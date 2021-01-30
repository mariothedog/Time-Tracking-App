from datetime import timedelta
import sched
import threading
import time

import psutil
from PyQt5.QtWidgets import QApplication
from win32gui import GetForegroundWindow, SetForegroundWindow, GetWindowText, GetWindowRect
from win32process import GetWindowThreadProcessId

from timer_window import TimerWindow

DELAY_LOG_ACTIVITY = 1

WINDOW_PADDING_X_RIGHT = 30

scheduler = sched.scheduler(time.time, time.sleep)

app = QApplication([])
window = TimerWindow()

seconds_spent = {}


def log_activity_action(last_hwnd=None):
    hwnd = GetForegroundWindow()
    name = None
    if hwnd:
        if GetWindowText(hwnd) == window.windowTitle():  # Prevent focus on timer window
            SetForegroundWindow(last_hwnd)
            hwnd = last_hwnd

        rect = GetWindowRect(hwnd)
        pos_x = rect[2] - window.width() - WINDOW_PADDING_X_RIGHT
        pos_y = rect[1] + window.height()
        window.move(pos_x, pos_y)

        pid = GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid)

        name = process.name()
        if name in seconds_spent:
            seconds_spent[name] += 1
        else:
            seconds_spent[name] = 0
        seconds = seconds_spent[name]
        window.label.setText(str(timedelta(seconds=seconds)))

    scheduler.enter(DELAY_LOG_ACTIVITY, 1, lambda: log_activity_action(hwnd))


def main():
    temp_hwnd = GetForegroundWindow()
    window.show()
    window.clearFocus()
    SetForegroundWindow(temp_hwnd)

    log_activity_action()

    scheduler_thread = threading.Thread(target=scheduler.run)
    scheduler_thread.start()
    app.exec_()


if __name__ == "__main__":
    main()
