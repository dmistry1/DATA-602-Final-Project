# -*- coding: utf-8 -*-
"""fireproj_updateDataDaily.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FPGNlx0GK6-7y0z8eBqo5XWaHrecgvGh
"""

#Need a way to find the most recent date and try to pull the combined fire and weather
# data for any dates missing up to today and then add them to the dataset
from google.colab import drive
drive.mount('/content/drive')

import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def update_data():
    # Get the current date
    cur_date = datetime.now().date()

    # Get the latest date available in our data
    file_path = '/content/drive/My Drive/combined_fire_weather_data_pastyr.csv'
    df = pd.read_csv(file_path)
    df['DATE'] = pd.to_datetime(df['DATE'])
    most_recent_date = df['DATE'].max().date()
    need_date = most_recent_date + timedelta(days=1)

    # Initialize DataFrame to store fire data
    all_fire_data = pd.DataFrame()

    # Iterate over each day and fetch fire data
    current_date = need_date
    while current_date <= cur_date:
        firm_api = f"https://firms.modaps.eosdis.nasa.gov//api/area/csv/33c0bb32b80831ae1cb4bb94211611c8/MODIS_NRT/world/1/{current_date.strftime('%Y-%m-%d')}"
        df_firm = pd.read_csv(firm_api)
        df_firm = df_firm[['acq_date', 'latitude', 'longitude', 'frp']]
        df_firm = df_firm[(df_firm['latitude'] >= 20.500) & (df_firm['latitude'] <= 21.0000)]
        df_firm = df_firm[(df_firm['longitude'] >= -156.5000) & (df_firm['longitude'] <= -156.0000)]
        df_firm = df_firm[df_firm['frp'] > 0]

        # If df_firm is empty after filtering, add a row with acq_date = current_date
        if df_firm.empty:
            new_row = pd.DataFrame({'acq_date': [current_date.strftime('%Y-%m-%d')],
                                    'latitude': [None],
                                    'longitude': [None],
                                    'frp': [None]})
            df_firm = pd.concat([df_firm, new_row], ignore_index=True)

        # Ensure the 'acq_date' column is in datetime format
        df_firm['acq_date'] = pd.to_datetime(df_firm['acq_date'])

        # Concatenate daily fire data to the main DataFrame
        all_fire_data = pd.concat([all_fire_data, df_firm])

        # Move to the next day
        current_date += timedelta(days=1)

    # Fetch weather data
    api_token = 'zgMwINDQNvylBcCiyyrymXezccJNOZyp'
    weather_url = f'https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-summary-of-the-day&stations=91190022516&startDate={need_date}&endDate={cur_date}&format=json'
    headers = {'token': api_token}
    weather_response = requests.get(weather_url, headers=headers)
    weather_data = pd.DataFrame()
    if weather_response.status_code == 200:
        weather_data = pd.DataFrame(weather_response.json())

    # Ensure the 'DATE' column in weather data is in datetime format
    weather_data['DATE'] = pd.to_datetime(weather_data['DATE'])

    # Merge the weather and fire data
    combined_fire_and_weather = pd.merge(weather_data, all_fire_data, left_on='DATE', right_on='acq_date', how='left')

    # Narrow down to specific columns
    columns_to_keep = ['DATE', 'WDSP', 'STATION', 'DEWP', 'PRCP', 'TEMP', 'frp', 'latitude', 'longitude']
    combined_fire_and_weather = combined_fire_and_weather[columns_to_keep]

    # Replace None with NaN in frp
    combined_fire_and_weather[['frp']] = combined_fire_and_weather[['frp']].replace({None: np.nan})

    # Replace None with specific values in latitude and longitude
    combined_fire_and_weather['latitude'] = combined_fire_and_weather['latitude'].replace({None: 20.88871})
    combined_fire_and_weather['longitude'] = combined_fire_and_weather['longitude'].replace({None: -156.43453})

    # Calculate past_day_fire_bin for the new data
    combined_fire_and_weather['past_day_fire_bin'] = combined_fire_and_weather['frp'].shift(1).fillna(0).apply(lambda x: 1 if x > 0 else 0)

    # Load the existing data
    file_path = '/content/drive/My Drive/combined_fire_weather_data_pastyr.csv'
    existing_data = pd.read_csv(file_path)
    existing_data['DATE'] = pd.to_datetime(existing_data['DATE'])

    # Append the new data to the existing data
    combined_data = pd.concat([existing_data, combined_fire_and_weather], ignore_index=True)

    # Format the DATE column as MM/DD/YYYY
    combined_data['DATE'] = combined_data['DATE'].dt.strftime('%m/%d/%Y')

    # Save the combined data back to CSV
    combined_data.to_csv(file_path, index=False)

    return combined_data

# Example usage
combined_data = update_data()
print(combined_data)