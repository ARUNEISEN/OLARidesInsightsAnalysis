import pandas as pd
import os

filePath = "./ola_data/OLA_DataSet.xlsx"

datafeed = pd.ExcelFile(filePath)
july_df = datafeed.parse("July")


july_df['Customer_Rating'].fillna(july_df['Customer_Rating'].mean(), inplace=True)

july_df['Driver_Ratings'].fillna(july_df['Driver_Ratings'].median(), inplace=True)

july_df['Payment_Method'].fillna('Unknown', inplace=True)

july_df['C_TAT'].fillna(-1, inplace=True)

july_df['V_TAT'].fillna(-1, inplace=True)

july_df['Incomplete_Rides'].fillna(0, inplace=True)

missing_values = july_df.isnull().sum()
print(f"---Total Number of missing values : {missing_values}")

missing_percentage = (missing_values/len(july_df)) * 100
print(f"---Total percentage of Missing values : {missing_percentage}")

missing_summary = pd.DataFrame({
    'Missing_Values': missing_values,
    'Missing_%': missing_percentage.round(2)
}).sort_values(by='Missing_%', ascending=False)

print(missing_summary)

output_folder = "./Cleaned_Data"

cleaned_file_path = os.path.join(output_folder, "Cleaned_OLA_Data.xlsx")
july_df.to_excel(cleaned_file_path, index=False)

cleaned_file_path = os.path.join(output_folder, "Cleaned_OLA_Data.csv")
july_df.to_csv(cleaned_file_path, index=False)

