from datetime import datetime

class Booking:
    def __init__(self, booking_id: str, flight_id: str, customer_id: str, booking_time: datetime, seat_number: str):
        self.booking_id = booking_id
        self.flight_id = flight_id
        self.customer_id = customer_id
        self.booking_time = booking_time
        self.seat_number = seat_number