import win32gui
from datetime import datetime

def enum_windows_callback(hwnd, log_file):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsIconic(hwnd):
        log_file.write(f"{datetime.now()}: {win32gui.GetWindowText(hwnd)}\n")

def main():
    with open("log.txt", "a") as log_file:
        while True:
            win32gui.EnumWindows(enum_windows_callback, log_file)

if __name__ == "__main__":
    main()