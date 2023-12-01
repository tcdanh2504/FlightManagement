import tkinter as tk
from tkinter import ttk, messagebox
from controllers.fightController import FlightController
from models.flight import Flight, FlightStatus
from datetime import datetime, timedelta
import random

class FlightWindow(tk.Frame):
    
    def __init__(self, back_callback, parent=None):
        tk.Frame.__init__(self, parent)
        self.back_callback = back_callback
        self.controller = FlightController()
        
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=0, sticky='ew')

        # Add buttons to the button frame
        back_button = tk.Button(button_frame, text="Back", command=self.go_back)
        back_button.pack(side=tk.LEFT)

        add_button = tk.Button(button_frame, text="Add flight", command=self.create_flight)
        add_button.pack(side=tk.LEFT)
        
        edit_button = tk.Button(button_frame, text="Edit flight", command=self.edit)
        edit_button.pack(side=tk.LEFT)
        
        delete_button = tk.Button(button_frame, text="Delete flight", command=self.delete)
        delete_button.pack(side=tk.LEFT)

        # Create a frame for the Treeview
        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky='nsew')

        # Make the Treeview frame expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add a Treeview to the Treeview frame
        self.tree = ttk.Treeview(tree_frame, columns=('Flight ID', 'Departure', 'Destination', 'Departure Time', 'Arrival Time', 'Seats', 'Available Seats', 'Airline', 'Flight Status', 'Price', 'Aircraft Type'), show='headings')

        for col in ('Flight ID', 'Departure', 'Destination', 'Departure Time', 'Arrival Time', 'Seats', 'Available Seats', 'Airline', 'Flight Status', 'Price', 'Aircraft Type'):
            self.tree.heading(col, text=col)

        for col in self.tree["columns"]:
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
        data = self.controller.read_flights()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for flight in data:
            self.tree.insert("", "end", values=(flight.flight_id, flight.departure, flight.destination, flight.departure_time, flight.arrival_time, flight.seats, flight.available_seats, flight.airline, flight.flight_status, flight.price, flight.aircraft_type))
            
    def create_flight(self):
        self.create_or_edit_flight()
        # Create a new window
        # window = tk.Toplevel()

        # # Create labels and entry fields for each attribute of the Flight class
        # labels = ['Flight ID', 'Departure', 'Destination', 'Departure Time', 'Arrival Time', 'Seats', 'Available Seats', 'Airline', 'Flight Status', 'Price', 'Aircraft Type']
        # entries = []
        # for label in labels:
        #     row = tk.Frame(window)
        #     row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        #     tk.Label(row, width=15, text=label, anchor='w').pack(side=tk.LEFT)
        #     if label == 'Flight Status':
        #         # Create a combobox for the flight status
        #         flight_status = tk.StringVar()
        #         combobox = ttk.Combobox(row, textvariable=flight_status)
        #         combobox['values'] = ('On time', 'Delayed', 'Cancelled')
        #         combobox.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        #         entries.append(flight_status)  # Append the StringVar, not the combobox
        #     else:
        #         entry = tk.Entry(row)
        #         entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        #         entries.append(entry)

        # # Create a button that creates the Flight object and appends it to the CSV file
        # def submit():
        #     flight_id, departure, destination, departure_time, arrival_time, seats, available_seats, airline, flight_status, price, aircraft_type = [entry.get() for entry in entries]
        #     departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
        #     arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")
        #     seats = int(seats)
        #     available_seats = int(available_seats)
        #     price = float(price)
        #     flight = Flight(flight_id, departure, destination, departure_time, arrival_time, seats, available_seats, airline, flight_status, price, aircraft_type)
        #     self.controller.append_flight(flight)
        #     self.load_data_from_file()
        #     window.destroy()

        # tk.Button(window, text='Submit', command=submit).pack(side=tk.LEFT, padx=5, pady=5)
        
    def create_or_edit_flight(self, flight=None):
        # Create a new window
        window = tk.Toplevel()

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
            departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S.%f")
            arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S.%f")
            seats = int(seats)
            available_seats = int(available_seats)
            price = float(price)
            new_flight = Flight(flight_id, departure, destination, departure_time, arrival_time, seats, available_seats, airline, flight_status, price, aircraft_type)
            if flight is None:
                self.controller.append_flight(new_flight)
            else:
                self.controller.edit_flight(new_flight)
            self.load_data_from_file()
            window.destroy()

        tk.Button(window, text='Submit', command=submit).pack(side=tk.LEFT, padx=5, pady=5)
    
    # def add_new_flights(self):
    #     airlines = ['Vietnam Airlines', 'Jetstar Pacific', 'Bamboo Airways', 'VietJet Air']
    #     aircraft_types = ['Airbus A320', 'Boeing 737', 'Airbus A350', 'Boeing 787']
    #     statuses = [ "On time", "Delayed", "Cancelled"]
    #     locations = ['Hanoi', 'Ho Chi Minh City', 'Da Nang', 'Hai Phong', 'Can Tho', 'Nha Trang', 'Phu Quoc']

    #     # Generate 100 flights
    #     for i in range(1, 101):
    #         flight_id = f'VN{i:03}'
    #         departure, destination = random.sample(locations, 2)
    #         departure_time = datetime.now() + timedelta(days=i)
    #         arrival_time = departure_time + timedelta(hours=2)
    #         seats = 200
    #         available_seats = random.randint(0, 200)
    #         airline = random.choice(airlines) 
    #         flight_status = random.choice(statuses)  
    #         price = random.randint(10, 50)* 100000
    #         aircraft_type = random.choice(aircraft_types)  

    #         # Create the Flight object
    #         flight = Flight(flight_id, departure, destination, departure_time, arrival_time, seats, available_seats, airline, flight_status, price, aircraft_type)
    #         self.controller.append_flight(flight)
    #     self.load_data_from_file()
        
    def edit(self):
        selected_row = self.tree.selection()
        item_values = self.tree.item(selected_row, 'values')
        
        if len(item_values) == 0:
            return
        flight_id, departure, destination, departure_time, arrival_time, seats, available_seats, airline, flight_status, price, aircraft_type = item_values
        departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S.%f")
        arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S.%f")
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
            self.controller.remove_flight(item_values[0])
            self.load_data_from_file()

    def start(self):
        self.mainloop()

    def go_back(self):
        self.pack_forget()
        self.back_callback()