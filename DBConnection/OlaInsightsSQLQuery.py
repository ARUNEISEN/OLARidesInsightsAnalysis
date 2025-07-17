import pandas as pd
import psycopg2 as psg

class OLARideSQLInsights:
    def __init__(self):
        self.connection = psg.connect(
            host="localhost",
            database="OlaRide_Insights",
            user="postgres",
            password="root"
        )
        self.cursor = self.connection.cursor()

    # 1. Retrieve all successful bookings:

    def getAllSuccessfulBookings(self):
        query = '''SELECT "Date","Booking_ID" ,"Booking_Status", "Customer_ID",  "Vehicle_Type",  "Pickup_Location", 
                         "Drop_Location","Booking_Value", "Payment_Method","Ride_Distance", "Driver_Ratings", "Customer_Rating"
                   FROM "OLA_Ride_Data"
                   WHERE "Booking_Status" = 'Success'
                '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows,columns=["Date","Booking_ID" ,"Booking_Status", "Customer_ID",  "Vehicle_Type",  "Pickup_Location", 
                                         "Drop_Location","Booking_Value", "Payment_Method","Ride_Distance", "Driver_Ratings", "Customer_Rating"])
        return df
     

    # 2. Find the average ride distance for each vehicle type:
    def getAverageRideDistanceByVehicleType(self):
        query = '''SELECT 
	                    "Vehicle_Type", 
	                     AVG("Ride_Distance") AS avg_ride_distance
                    FROM "OLA_Ride_Data"
                    WHERE "Ride_Distance" IS NOT NULL
                    GROUP BY "Vehicle_Type"
                    ORDER BY avg_ride_distance DESC;
                '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows,columns=["Vehicle_Type","avg_ride_distance"])
        return df
    
    # 3. Get the total number of cancelled rides by customers:

    def getCountOfRidesCancelByCustomer(self):
        query = '''SELECT
	                    COUNT(*) AS Total_Cancelled_by_Customers
                    FROM "OLA_Ride_Data"
                    WHERE "Booking_Status" = 'Canceled by Customer'
                '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result

    # 4. List the top 5 customers who booked the highest number of rides:

    def getTopFiveCustomerByNoOfRides(self):
        query = '''SELECT 
                        "Customer_ID",
                        COUNT(*) as "Total_Rides"
                    FROM "OLA_Ride_Data"
                    GROUP BY "Customer_ID"
                    ORDER BY "Total_Rides" desc
                    LIMIT 5
                '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows, columns = ["Customer_ID","Total_Rides"])
        return df

    # 5. Get the number of rides cancelled by drivers due to personal and car-related issues:

    def getNoOfRidesByDriversIssues(self):
        query = '''SELECT
	                    COUNT(*) as "Cancelled_by_Driver_Issues"
                    FROM "OLA_Ride_Data"
                    WHERE "Booking_Status" = 'Canceled by Driver' AND "Canceled_Rides_by_Driver" = 'Personal & Car related issue' 
                 '''
        
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result
    
    # 6. Find the maximum and minimum driver ratings for Prime Sedan bookings:

    def getMinMaxDriverRatings(self):
        query = '''SELECT
                        "Vehicle_Type",
                         MIN("Driver_Ratings") AS min_driver_rating,
                         MAX("Driver_Ratings") AS max_driver_rating
                    FROM "OLA_Ride_Data"
                    WHERE "Vehicle_Type" = 'Prime Sedan'
                    GROUP BY "Vehicle_Type"
                '''            
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows, columns=["Vehicle_Type","min_driver_rating", "max_driver_rating"])
        return df

    # 7.  Retrieve all rides where payment was made using UPI:
    def getAllRidesThroughUPI(self):
        query = '''SELECT
                       "Date","Booking_ID" ,"Booking_Status", "Customer_ID",  "Vehicle_Type",  "Pickup_Location", 
                        "Drop_Location","Booking_Value", "Payment_Method","Ride_Distance", "Driver_Ratings", "Customer_Rating"
                   FROM "OLA_Ride_Data"
                   WHERE "Payment_Method" = 'UPI'
                '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows, columns=["Date","Booking_ID" ,"Booking_Status", "Customer_ID",  "Vehicle_Type",  "Pickup_Location", 
                                         "Drop_Location","Booking_Value", "Payment_Method","Ride_Distance", "Driver_Ratings", "Customer_Rating"])
        return df
    
    # 8.  Find the average customer rating per vehicle type:
    def getAverageCustomerRatingByVehicleType(self):
        query = '''SELECT 
                        "Vehicle_Type",
                        AVG("Customer_Rating") AS Avg_Customer_Rating
                    FROM "OLA_Ride_Data"
                    WHERE "Customer_Rating" IS NOT NULL
                    GROUP BY "Vehicle_Type"
                    ORDER BY Avg_Customer_Rating DESC
                '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows,columns=["Vehicle_Type","Avg_Customer_Rating"])
        return df
    
    # 9. Calculate the total booking value of rides completed successfully:
    def getTotalBookingValueForSuccessRides(self):
        query = '''SELECT 
                        SUM("Booking_Value") AS Total_Booking_Value
                    FROM "OLA_Ride_Data"
                    WHERE "Booking_Status" IS NOT NULL AND "Booking_Status" = 'Success'
                    GROUP BY "Booking_Status"
                '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result
    
    # 10. List all incomplete rides along with the reason
    def getListAllIncompleteRides(self):
        query = '''SELECT 
                        "Booking_ID",
                        "Customer_ID",
                        "Vehicle_Type",
                        "Pickup_Location",
                        "Drop_Location",
                        "Incomplete_Rides",
                        "Incomplete_Rides_Reason"
                    FROM "OLA_Ride_Data"
                    WHERE "Incomplete_Rides" = 'Yes'
                '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows,columns=[ "Booking_ID", "Customer_ID", "Vehicle_Type","Pickup_Location","Drop_Location","Incomplete_Rides","Incomplete_Rides_Reason"])
        return df
    

    def getBookingValueForStatus(self):
         query = '''SELECT "Booking_Status",
                        SUM("Booking_Value") AS Total_Booking_Value
                    FROM "OLA_Ride_Data"
                    GROUP BY "Booking_Status"
                    ORDER BY Total_Booking_Value DESC;
                '''
         self.cursor.execute(query)
         rows = self.cursor.fetchall()
         df = pd.DataFrame(rows,columns=["Booking_Status","Total_Booking_Value"])
         return df
    
    def getBookingValueForPaymentMethod(self):
         query = '''SELECT "Payment_Method",
                        SUM("Booking_Value") AS Total_Booking_Value
                    FROM "OLA_Ride_Data"
                    GROUP BY "Payment_Method"
                    ORDER BY Total_Booking_Value DESC;
                '''
         self.cursor.execute(query)
         rows = self.cursor.fetchall()
         df = pd.DataFrame(rows,columns=["Payment_Method","Total_Booking_Value"])
         return df
    
    def getBookingValueForVehileType(self):
         query = '''SELECT "Vehicle_Type",
                        SUM("Booking_Value") AS Total_Booking_Value
                    FROM "OLA_Ride_Data"
                    GROUP BY "Vehicle_Type"
                    ORDER BY Total_Booking_Value DESC;
                '''
         self.cursor.execute(query)
         rows = self.cursor.fetchall()
         df = pd.DataFrame(rows,columns=["Vehicle_Type","Total_Booking_Value"])
         return df

    
osi = OLARideSQLInsights()
osi.getAllSuccessfulBookings()
osi.getAverageRideDistanceByVehicleType()
osi.getCountOfRidesCancelByCustomer()
osi.getTopFiveCustomerByNoOfRides()
osi.getNoOfRidesByDriversIssues()
osi.getMinMaxDriverRatings()
osi.getAllRidesThroughUPI()
osi.getAverageCustomerRatingByVehicleType()
osi.getTotalBookingValueForSuccessRides()
osi.getListAllIncompleteRides()
osi.getBookingValueForStatus()
osi.getBookingValueForPaymentMethod()
osi.getBookingValueForVehileType()
