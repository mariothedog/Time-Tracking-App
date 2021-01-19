import ctypes as ct
from ctypes import  windll

def getWindowTitle(hWnd):
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buff = ct.create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buff, length + 1)
    return buff.value if buff.value else None

def main():
    while True:
        hWnd = windll.user32.GetForegroundWindow()
        p = windll.user32.GetParent(hWnd)
        print("Active:", getWindowTitle(hWnd), "    Parent:", getWindowTitle(p))

if __name__ == "__main__":
    main()