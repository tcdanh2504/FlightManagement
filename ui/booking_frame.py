import tkinter as tk
from tkinter import ttk, messagebox
from controllers.bookingController import BookingController
from models.booking import Booking
from datetime import datetime
from utils.result import Result

class BookingWindow(tk.Frame):
    
    def __init__(self, back_callback, parent=None):
        tk.Frame.__init__(self, parent)
        self.back_callback = back_callback
        self.controller = BookingController()
        self.setup_ui()
        
    def setup_ui(self):
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=0, sticky='ew')

        # Add buttons to the button frame
        back_button = tk.Button(button_frame, text="Back", command=self.go_back)
        back_button.pack(side=tk.LEFT)

        add_button = tk.Button(button_frame, text="Add booking", command=self.create_or_edit_booking)
        add_button.pack(side=tk.LEFT)
        
        edit_button = tk.Button(button_frame, text="Edit booking", command=self.edit)
        edit_button.pack(side=tk.LEFT)
        
        delete_button = tk.Button(button_frame, text="Delete booking", command=self.delete)
        delete_button.pack(side=tk.LEFT)

        # Create a frame for the Treeview
        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky='nsew')

        # Make the Treeview frame expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add a Treeview to the Treeview frame
        self.tree = ttk.Treeview(tree_frame, columns=('Booking ID', 'Flight ID', 'Customer ID', 'Booking time', 'Seat number'), show='headings')

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        # Add a Scrollbar to the frame
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbarX = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure the Treeview to use the Scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbarX.set)
        self.load_data_from_file()

        self.tree.pack(fill=tk.BOTH, expand=True)
        
    def load_data_from_file(self):
        data = self.controller.read_bookings()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for booking in data:
            self.tree.insert("", "end", values=(booking.booking_id, booking.flight_id, booking.customer_id, booking.booking_time, booking.seat_number))
        
    def create_or_edit_booking(self, booking=None):
        window = tk.Toplevel()

        labels = ['Booking ID', 'Flight ID', 'Customer ID', 'Booking time', 'Seat number']
        entries = []
        for label in labels:
            row = tk.Frame(window)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            tk.Label(row, width=15, text=label, anchor='w').pack(side=tk.LEFT)
            entry = tk.Entry(row)
            if booking is not None:
                entry.insert(0, getattr(booking, label.replace(' ', '_').lower()))
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append(entry)

        def submit():
            booking_id, flight_id, customer_id, booking_time, seat_number = [entry.get() for entry in entries]
            booking_time = datetime.strptime(booking_time, "%Y-%m-%d %H:%M:%S")
            new_booking = Booking(booking_id, flight_id, customer_id, booking_time, seat_number)
            if booking is None:
                self.handle_state(self.controller.append_booking(new_booking))
            else:
                self.handle_state(self.controller.edit_booking(new_booking))
            self.load_data_from_file()
            window.destroy()

        tk.Button(window, text='Submit', command=submit).pack(side=tk.LEFT, padx=5, pady=5)
        
    def edit(self):
        selected_row = self.tree.selection()
        item_values = self.tree.item(selected_row, 'values')
        
        if len(item_values) == 0:
            return
        booking_id, flight_id, customer_id, booking_time, seat_number = item_values
        booking_time = datetime.strptime(booking_time, "%Y-%m-%d %H:%M:%S")
        booking = Booking(booking_id, flight_id, customer_id, booking_time, seat_number)
        self.create_or_edit_booking(booking)
    
    def delete(self):
        selected_row = self.tree.selection()
        item_values = self.tree.item(selected_row, 'values')
        
        if len(item_values) == 0:
            return
        result = messagebox.askquestion("Delete", "Are you sure you want to delete this item?", icon='warning')
        # Check the result
        if result == 'yes':
            self.handle_state(self.controller.remove_booking(item_values[0]))
            self.load_data_from_file()
            
    def handle_state(self, result: Result):
        if not(result.is_success()):
            messagebox.showerror("Error", result.error)

    def start(self):
        self.mainloop()

    def go_back(self):
        self.pack_forget()
        self.back_callback()