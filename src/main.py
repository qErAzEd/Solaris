import customtkinter
from src.gui import ClickerGUI

def main():
    root = customtkinter.CTk()
    app = ClickerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
