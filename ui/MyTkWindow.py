import tkinter as tk
from NextFrame import *

class MyTkWindow(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)  # ADDED parent argument.
        nextWin = NextWindow(self.show)
        NextScreen = tk.Button(self, text="Next", command=lambda: [self.pack_forget(), nextWin.pack(), nextWin.start()])
        NextScreen.pack()

    def start(self):
        self.mainloop()

    def show(self):
        self.pack()