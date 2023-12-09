import os
from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd

import getHistoricalMap
import getMLPrediction
import createFireMap
import pandas as pd
import requests
from datetime import datetime, timedelta
import numpy as np
import getGoogleBucket
import uploadToGCS
app = Flask(__name__)
cors = CORS(app)


@app.route('/historical_fire', methods=['POST'])
def receive_date():
    data = request.get_json()
    selected_date = data.get('selectedDate')
    getFireMap = getHistoricalMap.create_fire_map(selected_date)
    map_html = getFireMap._repr_html_()
    return render_template_string('{{ map_html|safe }}', map_html=map_html), 200, {'Content-Type': 'text/html'}


@app.route('/')
def mauiWildfire():
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
            current_date += timedelta(days=1)
            # Fetch weather data
            api_token = 'zgMwINDQNvylBcCiyyrymXezccJNOZyp'
            weather_url = f'https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-summary-of-the-day&stations=91190022516&startDate={need_date}&endDate={cur_date}&format=json'
            headers = {'token': api_token}
            weather_response = requests.get(weather_url, headers=headers)
            if len(weather_response.json()) != 0:
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

                uploadToGCS.upload_csv_to_gcs('combined_fire_weather_data_past_yr','combined_fire_weather_data_past_yr.csv', combined_data)

                # Updating the binary file
                fire_weather_ml_binary = getGoogleBucket.getData('fire_weather_dates_ml_binary')
                # Load or create the binary data DataFrame
                fire_weather_ml_binary['date'] = pd.to_datetime(fire_weather_ml_binary['date'])

                # Check for each day in combined_data if there was an FRP > 0
                combined_data['DATE'] = pd.to_datetime(combined_data['DATE'])
                new_rows = []
                for date in pd.date_range(start=fire_weather_ml_binary['date'].max() + timedelta(days=1), end=combined_data['DATE'].max()):
                    fire_exist = int(combined_data[combined_data['DATE'] == date]['frp'].max() > 0)
                    new_rows.append({'date': date, 'Fire_exist': fire_exist})

                # Concatenate new rows to the binary data DataFrame
                binary_data = pd.concat([fire_weather_ml_binary, pd.DataFrame(new_rows)], ignore_index=True)

                uploadToGCS.upload_csv_to_gcs('fire_weather_dates_ml_binary','fire_weather_dates_ml_binary.csv', binary_data)

    prediction  = getMLPrediction.getPrediction()
    map_maui = createFireMap.getFireMap(prediction)
    map_html = map_maui._repr_html_()
    return render_template_string('{{ map_html|safe }}', map_html=map_html), 200, {'Content-Type': 'text/html'}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))