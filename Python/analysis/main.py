import tkinter as tk
from ui import AuthApp


def main():
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
