import customtkinter
import os
import sys
import ctypes
import time
import random
import threading
from config import load_config, save_config
from keybind import setup_keybind

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

class ClickerGUI:
    def __init__(self, root, config_file="clicker_config.json"):
        self.app = root
        self.config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.clicking = False
        self.bind_mode = False
        self.bound_key = None
        self.setup_window()
        self.setup_widgets()
        self.load_initial_config()
        self.setup_keybind()

    def setup_window(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.app.geometry('600x400')
        self.app.resizable(False, False)
        self.app.title('AutoClicker')
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        icon_path = os.path.join(base_path, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.app.iconbitmap(icon_path)

    def setup_widgets(self):
        self.min_label = customtkinter.CTkLabel(self.app, text="Min CPS:", font=("Arial", 14))
        self.min_label.place(relx=0.1, rely=0.2, anchor="w")
        self.min_slider = customtkinter.CTkSlider(self.app, from_=1, to=20, command=self.min_changed, width=200, button_color="#7d1aa1", button_hover_color="#7d1aa1")
        self.min_slider.place(relx=0.3, rely=0.2, anchor="w")
        self.min_value = customtkinter.CTkEntry(self.app, width=50, height=30, state="disabled")
        self.min_value.place(relx=0.75, rely=0.2, anchor="center")

        self.max_label = customtkinter.CTkLabel(self.app, text="Max CPS:", font=("Arial", 14))
        self.max_label.place(relx=0.1, rely=0.35, anchor="w")
        self.max_slider = customtkinter.CTkSlider(self.app, from_=1, to=20, command=self.max_changed, width=200, button_color="#7d1aa1", button_hover_color="#7d1aa1")
        self.max_slider.place(relx=0.3, rely=0.35, anchor="w")
        self.max_value = customtkinter.CTkEntry(self.app, width=50, height=30, state="disabled")
        self.max_value.place(relx=0.75, rely=0.35, anchor="center")

        self.bind_button = customtkinter.CTkButton(self.app, text="Bind", command=self.bind_key, width=100, height=30, fg_color="#7d1aa1", hover=False)
        self.bind_button.place(relx=0.1, rely=0.5, anchor="w")
        self.bind_value = customtkinter.CTkLabel(self.app, text="", font=("Arial", 14))
        self.bind_value.place(relx=0.3, rely=0.5, anchor="w")

    def min_changed(self, val):
        val = int(float(val))
        max_val = int(self.max_slider.get())
        if val > max_val:
            self.min_slider.set(max_val)
            val = max_val
        self.min_value.configure(state="normal")
        self.min_value.delete(0, "end")
        self.min_value.insert(0, str(val))
        self.min_value.configure(state="disabled")
        save_config(self.config_file, min_cps=int(self.min_slider.get()), max_cps=int(self.max_slider.get()), bound_key=self.bound_key)

    def max_changed(self, val):
        val = int(float(val))
        min_val = int(self.min_slider.get())
        if val < min_val:
            self.max_slider.set(min_val)
            val = min_val
        self.max_value.configure(state="normal")
        self.max_value.delete(0, "end")
        self.max_value.insert(0, str(val))
        self.max_value.configure(state="disabled")
        save_config(self.config_file, min_cps=int(self.min_slider.get()), max_cps=int(self.max_slider.get()), bound_key=self.bound_key)

    def bind_key(self):
        if self.bind_mode:
            return
        self.bind_mode = True
        self.bind_button.configure(text="Press a key")
        self.bound_key = None
        self.bind_value.configure(text="Waiting...")
        self.app.after(5000, self.end_bind_mode)

    def end_bind_mode(self):
        if self.bind_mode:
            self.bind_mode = False
            if self.bound_key:
                self.bind_button.configure(text="Bind")
                self.bind_value.configure(text=self.bound_key.upper())
                save_config(self.config_file, min_cps=int(self.min_slider.get()), max_cps=int(self.max_slider.get()), bound_key=self.bound_key)
            else:
                self.bind_button.configure(text="Bind")
                self.bind_value.configure(text="None")

    def load_initial_config(self):
        min_cps, max_cps, key = load_config(self.config_file)
        self.min_slider.set(min_cps)
        self.max_slider.set(max_cps)
        self.bound_key = key
        self.min_value.configure(state="normal")
        self.min_value.delete(0, "end")
        self.min_value.insert(0, str(min_cps))
        self.min_value.configure(state="disabled")
        self.max_value.configure(state="normal")
        self.max_value.delete(0, "end")
        self.max_value.insert(0, str(max_cps))
        self.max_value.configure(state="disabled")
        self.bind_value.configure(text=key.upper() if key else "None")
        self.bind_button.configure(text="Bind")

    def setup_keybind(self):
        self.bind_mode = False
        self.clicking = False
        self.bound_key = None
        # This function in your keybind module must connect key events to toggle clicking
        setup_keybind(self)

    def toggle_clicking(self):
        if self.clicking:
            self.clicking = False
        else:
            self.clicking = True
            threading.Thread(target=autoclick_loop, args=(self,), daemon=True).start()
