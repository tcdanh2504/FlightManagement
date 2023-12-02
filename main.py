import tkinter as tk
from tkinter import ttk, font
from utils.color import Color
from ui.flight_frame import FlightWindow
from ui.customer_frame import CustomerWindow
from ui.booking_frame import BookingWindow

class MainWindow(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self['bg'] = Color.PRIMARY.value
        
        spacer = tk.Label(self, height=2)  
        spacer.pack()
        spacer['bg'] = Color.PRIMARY.value
        title = tk.Label(self, text="Flight management", font=("Arial", 32))
        title.pack(fill=tk.X) 
        title["fg"] = Color.WHITE.value
        title['bg'] = Color.PRIMARY.value

        button_frame = tk.Frame(self)
        button_frame['bg'] = Color.PRIMARY.value
        button_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)  # Make the frame expand to fill the window
        
        flight_window = FlightWindow(self.show)
        flight_button = self.custom_button(root=button_frame,text="Flights", command=lambda: [self.pack_forget(), flight_window.pack(fill=tk.BOTH, expand=True), flight_window.start()])
        
        customer_window = CustomerWindow(self.show)
        customer_button = self.custom_button(root=button_frame,text="Customers", command=lambda: [self.pack_forget(), customer_window.pack(fill=tk.BOTH, expand=True), customer_window.start()])
        
        booking_window = BookingWindow(self.show)
        booking_button = self.custom_button(root=button_frame,text="Bookings", command=lambda: [self.pack_forget(), booking_window.pack(fill=tk.BOTH, expand=True), booking_window.start()])

        analysis_button = self.custom_button(root=button_frame,text="Analysis", command=lambda: [self.pack_forget(), booking_window.pack(fill=tk.BOTH, expand=True), booking_window.start()])

        flight_button.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        customer_button.grid(row=0, column=1, sticky='nsew', padx=20, pady=20)
        booking_button.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
        analysis_button.grid(row=1, column=1, sticky='nsew', padx=20, pady=20)

        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
    def custom_button(self, root, text: str, command) -> tk.Button:
        button = tk.Button(root, text=text, command=command)
        button["font"] = font.Font(size=20)
        button["bg"] = Color.WHITE.value
        button["fg"] = Color.PRIMARY.value
        button["activebackground"] = Color.WHITE.value
        button["activeforeground"] = Color.PRIMARY.value
        return button

    def start(self):
        self.mainloop()

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.geometry("800x600")
main_window = MainWindow(root)
main_window.pack(fill=tk.BOTH, expand=True)
main_window.start()   
