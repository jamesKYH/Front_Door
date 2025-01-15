import streamlit as st
import pandas as pd
import FinanceDataReader as fdr 
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO 
import pandas as pd
import os
import plotly.express as px
import requests
from io import StringIO

# Function to load and filter CSV based on city and date
def load_and_filter_csv(url, city, start_date, end_date):
    response = requests.get(url)
    if response.status_code == 200:
        # Convert response content to pandas DataFrame
        csv_content = StringIO(response.content.decode('utf-8'))
        df = pd.read_csv(csv_content)

        # Ensure date column is in datetime format
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

        # Filter by city and date range
        filtered_df = df[(df['city'] == city) & (df['date'].between(start_date, end_date))]
        return filtered_df
    else:
        print(f"Failed to fetch CSV: HTTP {response.status_code}")
        return pd.DataFrame()

# Concatenate data for multiple months
def concat_monthly_data(base_url, city, start_month, end_month):
    all_data = []
    for month in pd.date_range(start=start_month, end=end_month, freq='MS').strftime('%Y%m'):
        # Generate the monthly URL
        monthly_url = base_url.replace('202311', month)
        print(f"Fetching data from: {monthly_url}")
        monthly_data = load_and_filter_csv(monthly_url, city, start_date=f"{month}01", end_date=f"{month}31")
        if not monthly_data.empty:
            all_data.append(monthly_data)

    if all_data:
        concatenated_df = pd.concat(all_data, ignore_index=True)
        return concatenated_df
    else:
        print("No data available for the specified range.")
        return pd.DataFrame()

# Input values
base_url = 'https://woori-fisa-bucket.s3.ap-northeast-2.amazonaws.com/fisa04-card/tbsh_gyeonggi_day_202311_ansan.csv'
city = 'pochun'  # Change to 'suwon' if needed
start_date = '20230101'
end_date = '20231231'

# Process data
result_df = concat_monthly_data(base_url, city, start_date, end_date)

# Save the result to a new CSV
if not result_df.empty:
    result_df.to_csv('filtered_concatenated_data.csv', index=False)
    print("Filtered data saved as 'filtered_concatenated_data.csv'")
else:
    print("No filtered data to save.")