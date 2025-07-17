import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

class OlaRidesDataDBCreation:
    def __init__(self):
        file_path = "./Cleaned_Data/Cleaned_OLA_Data.csv"
        self.ola_df = pd.read_csv(file_path)
        self.DB_USER = 'postgres'
        self.DB_PASSWORD = 'root'
        self.DB_HOST = 'localhost'
        self.DB_PORT = '5432'
        self.DB_NAME = 'OlaRide_Insights'

    def create_database(self):
        conn = psycopg2.connect(
            dbname='postgres',
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if the target DB exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.DB_NAME}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f'CREATE DATABASE "{self.DB_NAME}"')
            print(f"Database '{self.DB_NAME}' created.")
        else:
            print(f"Database '{self.DB_NAME}' already exists.")

        cursor.close()
        conn.close()
        
    def moveDFToDB(self):
        engine = create_engine( f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        df = self.ola_df
        df = self.setDataType(self.ola_df)
        table_name = 'OLA_Ride_Data'
        if df is not None and not df.empty:
             df.to_sql(table_name, engine , if_exists='replace', index = False)
             print(f'{table_name} Table created succesfully in the OlaRide_Insights Database')
        else:
            print("DataFrame is None or Empty so skipping DB insertion.")

    def setDataType(self, df):
        df["Date"] = pd.to_datetime(df["Date"])        
        df["Time"] = pd.to_datetime(df["Time"], format='%H:%M:%S', errors='coerce').dt.time
        df = df.astype({
            "Booking_ID": "string",
            "Booking_Status": "string",
            "Customer_ID": "string",
            "Vehicle_Type": "string",
            "Pickup_Location": "string",
            "Drop_Location": "string",
            "V_TAT": "float",
            "C_TAT": "float",
            "Canceled_Rides_by_Customer": "string",
            "Canceled_Rides_by_Driver": "string",
            "Incomplete_Rides": "string",
            "Incomplete_Rides_Reason": "string",
            "Booking_Value": "float",
            "Payment_Method": "string",
            "Ride_Distance": "float",
            "Driver_Ratings": "float",
            "Customer_Rating": "float",
            "Vehicle Images": "string"
        })
        return df

          

ordbc = OlaRidesDataDBCreation()
ordbc.create_database()
ordbc.moveDFToDB()