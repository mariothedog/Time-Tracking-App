import atexit
from datetime import datetime
import os
import sched
import time

import win32gui

DELAY_LOG_ACTIVITY = 1
DELAY_FLUSH_LOG = 5

scheduler = sched.scheduler(time.time, time.sleep)
log_file = open("log.txt", "a", encoding="utf-8")
atexit.register(log_file.close)


def enum_windows_callback(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(hwnd):
        text = win32gui.GetWindowText(hwnd)
        if text:
            log_file.write(f"{datetime.now()}: {text}\n")


def log_activity_action():
    win32gui.EnumWindows(enum_windows_callback, None)
    scheduler.enter(DELAY_LOG_ACTIVITY, 1, log_activity_action)


def flush_log_action():
    log_file.flush()
    os.fsync(log_file.fileno())
    scheduler.enter(DELAY_FLUSH_LOG, 1, flush_log_action)


def main():
    log_activity_action()
    flush_log_action()
    scheduler.run()


if __name__ == "__main__":
    main()
