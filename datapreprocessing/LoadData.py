import pandas as pd

filePath = "./ola_data/OLA_DataSet.xlsx"

datafeed = pd.ExcelFile(filePath)
july_df = datafeed.parse("July")
missing_values = july_df.isnull().sum()
print(f"---Total Number of missing values : {missing_values}")
missing_percentage = (missing_values/len(july_df)) * 100
print(f"---Total percentage of Missing values : {missing_percentage}")
missing_summary = pd.DataFrame({
    'Missing_Values': missing_values,
    'Missing_%': missing_percentage.round(2)
}).sort_values(by='Missing_%', ascending=False)

print("**************************************************************************************")
print(missing_summary)