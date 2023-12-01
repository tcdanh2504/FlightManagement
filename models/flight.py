from datetime import datetime
from enum import Enum

class FlightStatus(Enum):
    ON_TIME = "On time"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"

class Flight:
    def __init__(self, flight_id: str, departure: str, destination: str,
                 departure_time: datetime, arrival_time: datetime,
                 seats: int, available_seats: int, airline: str, 
                 flight_status: FlightStatus,
                 price: float, aircraft_type: str):
        self.flight_id = flight_id
        self.departure = departure
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.seats = seats
        self.available_seats = available_seats
        self.airline = airline
        self.flight_status = flight_status
        self.price = price
        self.aircraft_type = aircraft_type