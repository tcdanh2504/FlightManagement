import pandas as pd
import numpy as np
from models.flight import Flight

class FlightController:
    def __init__(self):
        self.file_path = "data/flights.csv"
        self.data = pd.read_csv(self.file_path)

    def read_file(self):
        flights = []
        for index, row in self.data.iterrows():
            flight = Flight.Flight(row['flight_id'], row['departure'], row['destination'], row['departure_time'], row['arrival_time'], row['seats'], row['available_seats'])
            flights.append(flight)
        return flights

    def add_flight(self, flight: Flight):
        row = {'flight_id': flight.flight_id, 'departure': flight.departure, 'destination': flight.destination, 'departure_time': flight.departure_time, 'arrival_time': flight.arrival_time, 'seats': flight.seats, 'available_seats': flight.available_seats}
        self.data = self.data.append(row, ignore_index=True)
        self.data.to_csv(self.file_path, index=False)

    def delete_flight(self, flight_id):
        self.data = self.data[self.data.flight_id != flight_id]
        self.data.to_csv(self.file_path, index=False)

    def edit_flight(self, flight):
        self.data.loc[self.data['flight_id'] == flight.flight_id, 'departure'] = flight.departure
        self.data.loc[self.data['flight_id'] == flight.flight_id, 'destination'] = flight.destination
        self.data.loc[self.data['flight_id'] == flight.flight_id, 'departure_time'] = flight.departure_time
        self.data.loc[self.data['flight_id'] == flight.flight_id, 'arrival_time'] = flight.arrival_time
        self.data.loc[self.data['flight_id'] == flight.flight_id, 'seats'] = flight.seats
        self.data.loc[self.data['flight_id'] == flight.flight_id, 'available_seats'] = flight.available_seats
        self.data.to_csv(self.file_path, index=False)