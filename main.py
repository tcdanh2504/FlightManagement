import tkinter as tk
from ui.flight_frame import FlightWindow
from ui.customer_frame import CustomerWindow
from ui.booking_frame import BookingWindow

class MainWindow(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Flight management", font=("Arial", 20))
        title.pack()
        
        flight_window = FlightWindow(self.show)
        flight_button = tk.Button(self, text=f"Flight", command=lambda: [self.pack_forget(), flight_window.pack(fill=tk.BOTH, expand=True), flight_window.start()])
        flight_button.pack()
        
        customer_window = CustomerWindow(self.show)
        customer_button = tk.Button(self, text=f"Customer", command=lambda: [self.pack_forget(), customer_window.pack(fill=tk.BOTH, expand=True), customer_window.start()])
        customer_button.pack()
        
        booking_window = BookingWindow(self.show)
        booking_button = tk.Button(self, text=f"Booking", command=lambda: [self.pack_forget(), booking_window.pack(fill=tk.BOTH, expand=True), booking_window.start()])
        booking_button.pack()

    def start(self):
        self.mainloop()

    def show(self):
        self.pack()

root = tk.Tk()
root.geometry("800x600")
main_window = MainWindow(root)
main_window.pack(fill=tk.BOTH, expand=True)
main_window.start()   
