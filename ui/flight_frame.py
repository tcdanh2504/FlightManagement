import tkinter as tk
from tkinter import ttk, messagebox, font
from utils.color import Color
from controllers.fight_controller import FlightController
from models.flight import Flight
from datetime import datetime
from utils.result import Result
import numpy as np
from tkcalendar import DateEntry

class FlightWindow(tk.Frame):
    
    def __init__(self, back_callback, parent=None):
        tk.Frame.__init__(self, parent)
        self.back_callback = back_callback
        self.controller = FlightController()
        self.data = self.controller.read_flights()
        self.setup_ui()
        
    def setup_ui(self):
        self["bg"] = Color.PRIMARY.value
        button_frame = tk.Frame(self)
        spacer = tk.Label(button_frame, height=1)  
        spacer["bg"] = Color.PRIMARY.value
        spacer.pack()
        button_frame.grid(row=0, column=0, sticky='ew')
        button_frame["bg"] = Color.PRIMARY.value
        
        def custom_button(root, text, command) -> tk.Button:
            button = tk.Button(root, text=text, command=command)
            button["font"] = font.Font(size=12)
            button["bg"] = Color.WHITE.value
            button["fg"] = Color.PRIMARY.value
            button["activebackground"] = Color.WHITE.value
            button["activeforeground"] = Color.PRIMARY.value
            return button

        # Add buttons to the button frame
        back_button = custom_button(button_frame, text="Back", command=self.go_back)
        back_button.pack(side=tk.LEFT, padx=10)

        add_button = custom_button(button_frame, text="Add flight", command=self.create_or_edit_flight)
        add_button.pack(side=tk.LEFT)
        
        edit_button = custom_button(button_frame, text="Edit flight", command=self.edit)
        edit_button.pack(side=tk.LEFT, padx=10)
        
        delete_button = custom_button(button_frame, text="Delete flight", command=self.delete)
        delete_button.pack(side=tk.LEFT)
        
        start_departure = tk.Label(button_frame, text="Min Departure", font=("Arial", 12))
        start_departure.pack(side=tk.LEFT, padx=10)
        start_departure["fg"] = Color.WHITE.value
        start_departure['bg'] = Color.PRIMARY.value
        
        start_date = DateEntry(button_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        min_departure_time = np.min([flight.departure_time for flight in self.data])
        start_date.pack(side=tk.LEFT)
        start_date.set_date(min_departure_time)
        
        def date_change(event):
            flights_mask = np.array([flight.departure_time.date() >= start_date.get_date() 
                                           and flight.arrival_time.date() <= end_date.get_date() for flight in self.data])
            self.load_data_to_table(self.data[flights_mask])
            
        start_date.bind("<<DateEntrySelected>>", date_change)
        
        end_arrival = tk.Label(button_frame, text="Max Arrival", font=("Arial", 12))
        end_arrival.pack(side=tk.LEFT, padx=10)
        end_arrival["fg"] = Color.WHITE.value
        end_arrival['bg'] = Color.PRIMARY.value
        
        end_date = DateEntry(button_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        max_arrival_time = np.max([flight.arrival_time for flight in self.data])
        end_date.pack(side=tk.LEFT)
        end_date.set_date(max_arrival_time)
            
        end_date.bind("<<DateEntrySelected>>", date_change)

        # Create a frame for the Treeview
        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Make the Treeview frame expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            try:
                l = [(float(val), k) for val, k in l]
            except ValueError:
                pass

            l.sort(reverse=reverse)

            # rearrange items in sorted positions
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            for i, item in enumerate(self.tree.get_children()):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.item(item, tags=(tag,))
            # reverse sort next time
            tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

        # Add a Treeview to the Treeview frame
        self.tree = ttk.Treeview(tree_frame, columns=('Flight ID', 'Departure', 'Destination', 'Departure Time', 'Arrival Time', 'Seats', 'Available Seats', 'Airline', 'Flight Status', 'Price', 'Aircraft Type'), show='headings')
        self.tree.tag_configure("evenrow", background=Color.FOUR.value) 
        self.tree.tag_configure("oddrow", background=Color.WHITE.value) 

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(self.tree, _col, False))
            self.tree.column(col, width=100)
        # Add a Scrollbar to the frame
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbarX = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure the Treeview to use the Scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbarX.set)
        self.load_data_to_table(self.data)

        self.tree.pack(fill=tk.BOTH, expand=True)
        
    def load_data_to_table(self, data):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for flight in data:
            self.tree.insert("", "end", values=(flight.flight_id, flight.departure, flight.destination, flight.departure_time, flight.arrival_time, flight.seats, flight.available_seats, flight.airline, flight.flight_status, flight.price, flight.aircraft_type))
        for i, item in enumerate(self.tree.get_children()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.item(item, tags=(tag,))
        
    def create_or_edit_flight(self, flight=None):
        # Create a new window
        window = tk.Toplevel()
        window["bg"] = Color.PRIMARY.value

        # Create labels and entry fields for each attribute of the Flight class
        labels = ['Flight ID', 'Departure', 'Destination', 'Departure Time', 'Arrival Time', 'Seats', 'Available Seats', 'Airline', 'Flight Status', 'Price', 'Aircraft Type']
        entries = []
        for label in labels:
            row = tk.Frame(window)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            tk.Label(row, width=15, text=label, anchor='w').pack(side=tk.LEFT)
            if label == 'Flight Status':
                # Create a combobox for the flight status
                flight_status = tk.StringVar()
                combobox = ttk.Combobox(row, textvariable=flight_status)
                combobox['values'] = ('On time', 'Delayed', 'Cancelled')
                if flight is not None:
                    combobox.set(getattr(flight, label.replace(' ', '_').lower()))
                combobox.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                entries.append(flight_status)  # Append the StringVar, not the combobox
            else:
                entry = tk.Entry(row)
                if flight is not None:
                    entry.insert(0, getattr(flight, label.replace(' ', '_').lower()))
                entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                entries.append(entry)

        # Create a button that creates the Flight object and appends it to the CSV file
        def submit():
            flight_id, departure, destination, departure_time, arrival_time, seats, available_seats, airline, flight_status, price, aircraft_type = [entry.get() for entry in entries]
            departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
            arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")
            seats = int(seats)
            available_seats = int(available_seats)
            price = float(price)
            new_flight = Flight(flight_id, departure, destination, departure_time, arrival_time, seats, available_seats, airline, flight_status, price, aircraft_type)
            if flight is None:
                self.handle_state(self.controller.append_flight(new_flight))
            else:
                self.handle_state(self.controller.edit_flight(new_flight))
            self.load_data_from_file()
            window.destroy()

        tk.Button(window, text='Submit', command=submit).pack(side=tk.LEFT, padx=5, pady=5)
        
    def edit(self):
        selected_row = self.tree.selection()
        item_values = self.tree.item(selected_row, 'values')
        
        if len(item_values) == 0:
            return
        flight_id, departure, destination, departure_time, arrival_time, seats, available_seats, airline, flight_status, price, aircraft_type = item_values
        departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
        arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")
        seats = int(seats)
        available_seats = int(available_seats)
        price = float(price)
        flight = Flight(flight_id, departure, destination, departure_time, arrival_time, seats, available_seats, airline, flight_status, price, aircraft_type)
        self.create_or_edit_flight(flight)
    
    def delete(self):
        selected_row = self.tree.selection()
        item_values = self.tree.item(selected_row, 'values')
        
        if len(item_values) == 0:
            return
        result = messagebox.askquestion("Delete", "Are you sure you want to delete this item?", icon='warning')
        # Check the result
        if result == 'yes':
            self.handle_state(self.controller.remove_flight(item_values[0]))
            self.load_data_from_file()
            
    def handle_state(self, result: Result):
        if not(result.is_success()):
            messagebox.showerror("Error", result.error)

    def start(self):
        self.mainloop()

    def go_back(self):
        self.pack_forget()
        self.back_callback()