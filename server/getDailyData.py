import pandas as pd
import requests
from datetime import datetime, timedelta
import numpy as np
from urllib import request, error
import getGoogleBucket
import uploadToGCS

# Get the current date
cur_date = datetime.now().date()

combinedFireWeatherData = getGoogleBucket.getData('combined_fire_weather_data_past_yr')
two_days_ago = cur_date - timedelta(days=2)
# Get the latest date available in our data
combinedFireWeatherData['DATE'] = pd.to_datetime(combinedFireWeatherData['DATE'])
most_recent_date = combinedFireWeatherData['DATE'].max().date()
need_date = most_recent_date + timedelta(days=1)
# Initialize DataFrame to store fire data
all_fire_data = pd.DataFrame()

# Iterate over each day and fetch fire data
current_date = need_date
if two_days_ago != most_recent_date:
    while current_date <= cur_date:
        firm_api = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/33c0bb32b80831ae1cb4bb94211611c8/MODIS_NRT/world/1/{current_date.strftime('%Y-%m-%d')}"
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
        print('current_data', current_date)
        current_date += timedelta(days=1)
        # Fetch weather data
        api_token = 'zgMwINDQNvylBcCiyyrymXezccJNOZyp'
        weather_url = f'https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-summary-of-the-day&stations=91190022516&startDate={need_date}&endDate={cur_date}&format=json'
        headers = {'token': api_token}
        weather_response = requests.get(weather_url, headers=headers)
        print('inside the second if')
        weather_data = pd.DataFrame()
        weather_data = pd.DataFrame(weather_response.json())
        # Ensure the 'DATE' column in weather data is in datetime format
        weather_data['DATE'] = pd.to_datetime(weather_data['DATE'])

        # # Merge the weather and fire data
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
        # downloadCSV.download_csv_from_gcs('combined_fire_weather_data_past_yr', 'combined_fire_weather_data_past_yr.csv')
        # Append the new data to the existing data
        combined_data = pd.concat([combinedFireWeatherData, combined_fire_and_weather], ignore_index=True)

        # Format the DATE column as MM/DD/YYYY
        combined_data['DATE'] = combined_data['DATE'].dt.strftime('%m/%d/%Y')

        response = uploadToGCS.upload_csv_to_gcs('combined_fire_weather_data_past_yr','combined_fire_weather_data_past_yr.csv', combined_data)