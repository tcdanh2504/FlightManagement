import tkinter as tk

class NextWindow(tk.Frame):
    def __init__(self, back_callback, parent=None):
        tk.Frame.__init__(self, parent)  # ADDED parent argument.
        self.back_callback = back_callback
        Leave = tk.Button(self, text="Back", command=self.go_back)
        Leave.pack()

    def start(self):
        self.mainloop()

    def go_back(self):
        self.pack_forget()
        self.back_callback()