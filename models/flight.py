class Flight:
    def __init__(self, flight_id, departure, destination, departure_time, arrival_time, seats, available_seats):
        self.flight_id = flight_id
        self.departure = departure
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.seats = seats
        self.available_seats = available_seats