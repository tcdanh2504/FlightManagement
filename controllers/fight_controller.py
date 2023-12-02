import pandas as pd
from typing import List
from models.flight import Flight
from utils.result import Result

class FlightController:
    def __init__(self):
        self.csv_file = "data/flights.csv"

    def append_flight(self, flight: Flight) -> Result:
        # Create a DataFrame from the flight object's attributes
        flight_df = pd.DataFrame([vars(flight)])
        is_file_exist = True

        # Try to read the existing CSV file
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            # If the file doesn't exist, create a new one
            is_file_exist = False
            df = pd.DataFrame()

        # Check if the flight ID already exists
        if is_file_exist and df['flight_id'].isin([flight.flight_id]).any():
            return Result(error=f"Flight ID {flight.flight_id} already exists.")
        else:
            # Append the new flight data
            df = df.append(flight_df, ignore_index=True)

            # Write the DataFrame back to the CSV file
            df.to_csv(self.csv_file, index=False)
            return Result(data="Flight added successfully.")

    def read_flights(self) -> List[Flight]:
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(self.csv_file)
            df['departure_time'] = pd.to_datetime(df['departure_time'])
            df['arrival_time'] = pd.to_datetime(df['arrival_time'])
            # Convert the DataFrame to a list of Flight objects
            flights = [Flight(**flight) for flight in df.to_dict('records')]
        except FileNotFoundError:
            # If the file doesn't exist, return an empty list
            flights = []

        return flights
    
    def remove_flight(self, flight_id: str) -> Result:
        # Try to read the existing CSV file
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            return Result(error="File not found.")

        # Check if the flight ID exists
        if not df['flight_id'].isin([flight_id]).any():
            return Result(error=f"Flight ID {flight_id} does not exist.")
        else:
            # Remove the flight with the given ID
            df = df[df.flight_id != flight_id]

            # Write the DataFrame back to the CSV file
            df.to_csv(self.csv_file, index=False)
            return Result(data="Flight removed successfully.")

    def edit_flight(self, flight: Flight) -> Result:
        # Try to read the existing CSV file
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            return Result(error="File not found.")

        # Check if the flight ID exists
        if not df['flight_id'].isin([flight.flight_id]).any():
            return Result(error=f"Flight ID {flight.flight_id} does not exist.")
        else:
            # Find the index of the flight with the given ID
            index = df[df['flight_id'] == flight.flight_id].index[0]

            # Update the flight data
            for key, value in vars(flight).items():
                if key in df.columns:
                    df.loc[index, key] = value

            # Write the DataFrame back to the CSV file
            df.to_csv(self.csv_file, index=False)
            return Result(data="Flight edited successfully.")