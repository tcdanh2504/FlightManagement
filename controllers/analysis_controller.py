import pandas as pd
from typing import List
from models.flight import Flight
from utils.result import Result
from utils.constants import BOOKING_CSV_FILE, FLIGHT_CSV_FILE, CUSTOMER_CSV_FILE

class AnalysisController():
    def get_flights_pd(self):
        return pd.read_csv(FLIGHT_CSV_FILE)
    
    def get_bookings_pd(self):
        return pd.read_csv(BOOKING_CSV_FILE)