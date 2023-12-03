import pandas as pd
from typing import List
from models.booking import Booking
from utils.result import Result
from utils.constants import BOOKING_CSV_FILE, FLIGHT_CSV_FILE, CUSTOMER_CSV_FILE

class BookingController:
    def __init__(self):
        self.csv_file = BOOKING_CSV_FILE

    def append_booking(self, booking: Booking) -> Result:
        booking_df = pd.DataFrame([vars(booking)])
        is_file_exist = True
        
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            is_file_exist = False
            df = pd.DataFrame()

        # Check if the flight_id and customer_id are valid
        flight_df = pd.read_csv(FLIGHT_CSV_FILE)
        customer_df = pd.read_csv(CUSTOMER_CSV_FILE)
        if not flight_df['flight_id'].isin([booking.flight_id]).any():
            return Result(error=f"Flight ID {booking.flight_id} does not exist.")
        elif not customer_df['customer_id'].isin([booking.customer_id]).any():
            return Result(error=f"Customer ID {booking.customer_id} does not exist.")
        elif df['booking_id'].isin([booking.booking_id]).any():
            return Result(error=f"Booking ID {booking.booking_id} already exists.")
        # Check if the customer_id has already booked the flight_id
        elif is_file_exist and df[(df['customer_id'] == booking.customer_id) & (df['flight_id'] == booking.flight_id)].shape[0] > 0:
            return Result(error=f"Customer ID {booking.customer_id} has already booked Flight ID {booking.flight_id}.")
        else:
            df = df.append(booking_df, ignore_index=True)
            df.to_csv(self.csv_file, index=False)
            return Result(data="Booking added successfully.")

    def read_bookings(self) -> List[Booking]:
        try:
            df = pd.read_csv(self.csv_file)
            df['booking_time'] = pd.to_datetime(df['booking_time'])
            bookings = [Booking(**booking) for booking in df.to_dict('records')]
        except FileNotFoundError:
            bookings = []

        return bookings
    
    def remove_booking(self, booking_id: str) -> Result:
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            return Result(error="File not found.")

        if not df['booking_id'].isin([booking_id]).any():
            return Result(error=f"Booking ID {booking_id} does not exist.")
        else:
            df = df[df.booking_id != booking_id]
            df.to_csv(self.csv_file, index=False)
            return Result(data="Booking removed successfully.")

    def edit_booking(self, booking: Booking) -> Result:
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            return Result(error="File not found.")

        # Check if the flight_id and customer_id are valid
        flight_df = pd.read_csv("data/flights.csv")
        customer_df = pd.read_csv("data/customers.csv")
        if not flight_df['flight_id'].isin([booking.flight_id]).any():
            return Result(error=f"Flight ID {booking.flight_id} does not exist.")
        elif not customer_df['customer_id'].isin([booking.customer_id]).any():
            return Result(error=f"Customer ID {booking.customer_id} does not exist.")

        if not df['booking_id'].isin([booking.booking_id]).any():
            return Result(error=f"Booking ID {booking.booking_id} does not exist.")
        else:
            # Find the index of the booking with the given ID
            index = df[df['booking_id'] == booking.booking_id].index[0]

            # Check if the customer_id has already booked the flight_id
            if df[(df['customer_id'] == booking.customer_id) & (df['flight_id'] == booking.flight_id) & (df.index != index)].shape[0] > 0:
                return Result(error=f"Customer ID {booking.customer_id} has already booked Flight ID {booking.flight_id}.")
            else:
                # Update the booking data
                for key, value in vars(booking).items():
                    if key in df.columns:
                        df.loc[index, key] = value

                df.to_csv(self.csv_file, index=False)
                return Result(data="Booking edited successfully.")