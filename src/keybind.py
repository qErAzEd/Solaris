import threading
import pynput.keyboard
from .mouse import autoclick_loop

def setup_keybind(gui):
    def on_key_press(key):
        if gui.bind_mode:
            try:
                gui.bound_key = key.char
            except AttributeError:
                gui.bound_key = str(key).replace("Key.", "")
            gui.bind_mode = False
            gui.app.after(0, lambda: gui.bind_button.configure(text="Bind"))
            gui.app.after(0, lambda: gui.bind_value.configure(text=gui.bound_key.upper()))
            from .config import save_config
            save_config(gui.config_file, min_cps=int(gui.min_slider.get()), max_cps=int(gui.max_slider.get()), bound_key=gui.bound_key)
            return
        if gui.bound_key is None:
            return
        try:
            k = key.char
        except AttributeError:
            k = str(key).replace("Key.", "")
        if k == gui.bound_key:
            if not gui.clicking:
                gui.clicking = True
                gui.click_thread = threading.Thread(target=autoclick_loop, args=(gui,), daemon=True)
                gui.click_thread.start()
            else:
                gui.clicking = False

    gui.keyboard_listener = pynput.keyboard.Listener(on_press=on_key_press)
    gui.keyboard_listener.start()
