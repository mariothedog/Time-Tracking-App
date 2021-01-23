from datetime import timedelta
import sched
import threading
import time

import psutil
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from win32gui import GetForegroundWindow, GetWindowText, MoveWindow
from win32process import GetWindowThreadProcessId

from timer_window import TimerWindow

DELAY_LOG_ACTIVITY = 1
DELAY_FLUSH_LOG = 5

scheduler = sched.scheduler(time.time, time.sleep)

app = QApplication([])
window = TimerWindow()

seconds_spent = {}


def log_activity_action(last_process=None):
    hwnd = GetForegroundWindow()
    name = None
    if hwnd and GetWindowText(hwnd) != window.windowTitle():
        pid = GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid)

        name = process.name()
        if name != last_process:  # TODO: Move window
            pass
        if name in seconds_spent:
            seconds_spent[name] += 1
        else:
            seconds_spent[name] = 0
        seconds = seconds_spent[name]
        window.label.setText(str(timedelta(seconds=seconds)))

    scheduler.enter(DELAY_LOG_ACTIVITY, 1, lambda: log_activity_action(name))


def main():
    window.show()
    window.clearFocus()

    log_activity_action()

    scheduler_thread = threading.Thread(target=scheduler.run)
    scheduler_thread.start()
    app.exec_()


if __name__ == "__main__":
    main()
