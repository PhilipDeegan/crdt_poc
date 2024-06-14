import atexit
import os
import sys
import termios
import tty

base_settings_ = termios.tcgetattr(sys.stdin)


@atexit.register
def shutdown():
    """reset terminal to not hide inputs"""
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, base_settings_)


_key_mapping = {
    127: "backspace",
    10: "return",
    32: "space",
    9: "tab",
    27: "esc",
    65: "up",
    66: "down",
    67: "right",
    68: "left",
}


def getkey():
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            print("k", b)
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b)
            return _key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, base_settings_)


def poll():
    s = ""
    while True:
        try:
            k = getkey()
            if k == "esc":
                quit()
            elif k == "return":
                print(s)
                return s
            else:
                s += k
        except (KeyboardInterrupt, SystemExit):
            os.system("stty sane")
            print("bad!")
