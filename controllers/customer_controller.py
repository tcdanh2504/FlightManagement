import pandas as pd
from typing import List
from models.customer import Customer
from utils.result import Result
from utils.constants import CUSTOMER_CSV_FILE

class CustomerController:
    def __init__(self):
        self.csv_file = CUSTOMER_CSV_FILE

    def append_customer(self, customer: Customer) -> Result:
        customer_df = pd.DataFrame([vars(customer)])
        is_file_exist = True

        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            is_file_exist = False
            df = pd.DataFrame()

        if is_file_exist and df['customer_id'].isin([customer.customer_id]).any():
            return Result(error=f"Customer ID {customer.customer_id} already exists.")
        else:
            df = df.append(customer_df, ignore_index=True)
            df.to_csv(self.csv_file, index=False)
            return Result(data="Customer added successfully.")

    def read_customers(self) -> List[Customer]:
        try:
            df = pd.read_csv(self.csv_file)
            customers = [Customer(**customer) for customer in df.to_dict('records')]
        except FileNotFoundError:
            customers = []

        return customers

    def remove_customer(self, customer_id: str) -> Result:
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            return Result(error="File not found.")

        if not df['customer_id'].isin([customer_id]).any():
            return Result(error=f"Customer ID {customer_id} does not exist.")
        else:
            df = df[df.customer_id != customer_id]
            df.to_csv(self.csv_file, index=False)
            return Result(data="Customer removed successfully.")

    def edit_customer(self, customer: Customer) -> Result:
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            return Result(error="File not found.")

        if not df['customer_id'].isin([customer.customer_id]).any():
            return Result(error=f"Customer ID {customer.customer_id} does not exist.")
        else:
            index = df[df['customer_id'] == customer.customer_id].index[0]

            for key, value in vars(customer).items():
                if key in df.columns:
                    df.loc[index, key] = value

            df.to_csv(self.csv_file, index=False)
            return Result(data="Customer edited successfully.")
