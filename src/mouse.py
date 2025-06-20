import ctypes
import time
import random

def send_mouse_click():
    user32 = ctypes.windll.user32
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def autoclick_loop(gui):
    while gui.clicking:
        min_cps = int(gui.min_slider.get())
        max_cps = int(gui.max_slider.get())
        if min_cps > max_cps:
            min_cps, max_cps = max_cps, min_cps
        low = max(1, min_cps - 1)
        high = min(20, max_cps + 1)
        cps = random.randint(low, high)
        interval = 1 / cps
        send_mouse_click()
        time.sleep(interval)
