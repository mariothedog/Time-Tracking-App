import atexit
from datetime import datetime
import os
import sched
import time

import psutil
import win32gui
import win32process

DELAY_LOG_ACTIVITY = 1
DELAY_FLUSH_LOG = 5

scheduler = sched.scheduler(time.time, time.sleep)
log_file = open("log.txt", "a", encoding="utf-8")
atexit.register(log_file.close)


def log_activity_action():
    hwnd = win32gui.GetForegroundWindow()
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    process = psutil.Process(pid)
    log_file.write(f"{datetime.now()}: {process.name()}\n")
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
