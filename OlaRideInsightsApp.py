import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

from DBConnection.OlaInsightsSQLQuery import OLARideSQLInsights

st.set_page_config(page_title="OLA Insights", layout="wide")
st.title("OLA RIDE INSIGHTS")
st.sidebar.title("OLA Ride Insights Sections")

selectRB = st.sidebar.radio(
    "Business Case Studies",
    options = 
    ["Home",
    "Insights"
    ]
)

ola_results = OLARideSQLInsights()
if selectRB == "Home":
    bookstatus_df = ola_results.getBookingValueForStatus()
    bookpay_df = ola_results.getBookingValueForPaymentMethod()
    bookVehile_df = ola_results.getBookingValueForVehileType()
    fig1 = px.pie(bookstatus_df, names="Booking_Status", values="Total_Booking_Value", title="Booking Status VS booking value")
    fig2 = px.pie(bookpay_df, names="Payment_Method", values="Total_Booking_Value", title="Payment Types VS booking value")
    fig3 = px.pie(bookVehile_df, names="Vehicle_Type", values="Total_Booking_Value", title="Vehicle Types VS booking value")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        st.plotly_chart(fig3, use_container_width=True)
   
if selectRB == "Insights":
    col1, col2 = st.columns([3,1])
    with col1:
        st.subheader("Ola Ride Insights")        
        if st.checkbox("List all successful bookings"):
            df = ola_results.getAllSuccessfulBookings()
            if df.empty:
                st.warning("No Data available to display")
            st.dataframe(df)
        if st.checkbox("Show average ride distance by vehicle type"):
            df = ola_results.getAverageRideDistanceByVehicleType()
            if df.empty:
                st.warning("No Data available to display")
            st.dataframe(df)

            st.subheader("Avg Ride Distance vs Vehicle")
            fig, ax = plt.subplots(figsize=(12,6))
            ax.barh(df["Vehicle_Type"],df["avg_ride_distance"],color="seagreen")
            ax.set_xlabel("avg_ride_distance")
            ax.set_ylabel("Vehicle_Type")
            ax.set_title("Avg Ride Distance vs Vehicle")
            ax.invert_yaxis()
            st.pyplot(fig)
        if st.checkbox("Display number of rides cancelled by customers"):
            cancelled_count = ola_results.getCountOfRidesCancelByCustomer()
            st.markdown(
                        f"""
                        <div style='text-align: center; padding: 10px; border-radius: 10px;
                                    background-color: #ffe6e6; border: 2px solid #ff4d4d;'>
                            <h2 style='color: #cc0000; font-size: 36px; margin: 0;'>Rides Cancelled by Customers</h2>
                            <p style='font-size: 48px; color: #b30000; margin: 0;'>{cancelled_count}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        if st.checkbox("Show top 5 customers by ride count"):
            df = ola_results.getTopFiveCustomerByNoOfRides()
            if df.empty:
                st.warning("No Data available to display")
            st.dataframe(df)

            st.subheader("Top Five Customers VS Ride count")
            fig = px.bar(
                    df,
                    x='Total_Rides',
                    y='Customer_ID',
                    orientation='h',
                    title='Top 5 Customers by Number of Rides',
                    color='Total_Rides',
                    color_continuous_scale='Aggrnyl',
                    labels={'Customer_ID': 'Customer ID', 'Total_Rides': 'Number of Rides'}
                )

            fig.update_layout(yaxis=dict(autorange="reversed"))  # Highest on top
            st.plotly_chart(fig, use_container_width=True)
            
        if st.checkbox("Show driver cancellations due to personal or car issues"):
            cancelled_count = ola_results.getNoOfRidesByDriversIssues()
            st.markdown(
                        f"""
                           <div style='text-align: center; padding: 10px; border-radius: 10px;
                            background-color: #f3e6ff; border: 2px solid #9933cc;'>
                            <h2 style='color: #660099; font-size: 36px; margin: 0;'>Rides Cancelled by Customers</h2>
                              <p style='font-size: 48px; color: #4d0080; margin: 0;'>{cancelled_count}</p>
                            </div>
                        """,
                        unsafe_allow_html=True
                    )
        if st.checkbox("Show highest and lowest driver ratings for Prime Sedan"):
            df = ola_results.getMinMaxDriverRatings()
            min_rating = df.loc[0, "min_driver_rating"]
            max_rating = df.loc[0, "max_driver_rating"]

            st.subheader(f"Driver Ratings for {df.loc[0, 'Vehicle_Type']}")
            st.markdown(f"""
                        <div style='display: flex; justify-content: center; gap: 40px;'>
                            <div style='background-color: #e6f7ff; padding: 20px; border-radius: 12px; text-align: center; width: 200px;'>
                                <h3 style='color: #007acc;'>Minimum Rating</h3>
                                <p style='font-size: 36px; color: #005b99; margin: 0;'>{min_rating}</p>
                            </div>
                            <div style='background-color: #fff0f6; padding: 20px; border-radius: 12px; text-align: center; width: 200px;'>
                                <h3 style='color: #cc3300;'>Maximum Rating</h3>
                                <p style='font-size: 36px; color: #991f00; margin: 0;'>{max_rating}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        if st.checkbox("Show all UPI payment rides"):
            df = ola_results.getAllRidesThroughUPI()
            if df.empty:
                st.warning("No Data available to display")
            st.dataframe(df)
        if st.checkbox("Show average customer Rating by vehicle type"):
            df = ola_results.getAverageCustomerRatingByVehicleType()
            if df.empty:
                st.warning("No Data available to display")
            st.dataframe(df)
        if st.checkbox("Show total booking value of successful rides"):
            booking_value = ola_results.getTotalBookingValueForSuccessRides()
            st.markdown(
                        f"""
                          <div style='text-align: center; padding: 10px; border-radius: 10px;
                                background-color: #e6fff0; border: 2px solid #33cc66;'>
                            <h2 style='color: #269926; font-size: 36px; margin: 0;'>Total booking value of Successfull rides</h2>
                                <p style='font-size: 48px; color: #1a7a1a; margin: 0;'>{booking_value}</p>
                           </div>
                        """,
                        unsafe_allow_html=True
                    )
        if st.checkbox("List all incomplete rides with the reason"):
            df = ola_results.getListAllIncompleteRides()
            if df.empty:
                st.warning("No Data available to display")
            st.dataframe(df)