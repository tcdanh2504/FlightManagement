import tkinter as tk
from ui.flight_frame import FlightWindow

class MainWindow(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Flight management", font=("Arial", 20))
        title.pack()
        
        flight_window = FlightWindow(self.show)
        flight_button = tk.Button(self, text=f"Flight", command=lambda: [self.pack_forget(), flight_window.pack(fill=tk.BOTH), flight_window.start()])
        flight_button.pack()
        
        customer_button = tk.Button(self, text=f"Customer")
        customer_button.pack()
        booking_button = tk.Button(self, text=f"Booking")
        booking_button.pack()

    def start(self):
        self.mainloop()

    def show(self):
        self.pack()

root = tk.Tk()
root.geometry("800x600")
main_window = MainWindow(root)
main_window.pack(fill=tk.BOTH)
main_window.start()   
