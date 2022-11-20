import tkinter as tk
from GUI import gui


if __name__ == '__main__':
    window = tk.Tk()
    application = gui(window)
    window.mainloop()
