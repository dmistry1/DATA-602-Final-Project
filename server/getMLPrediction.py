import getGoogleBucket
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def getPrediction():
    # Loads both of the csv from google cloud storage
    df_weather = getGoogleBucket.getData('combined_fire_weather_data_past_yr')
    df_fire = getGoogleBucket.getData('fire_weather_dates_ml_binary')

    # Include DATE in df_weather for merging, but it's not a feature for training
    columns_to_use = ['DATE', 'TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']
    df_weather = df_weather[columns_to_use]

    # Convert 'DATE' columns to datetime
    df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])
    df_fire['DATE'] = pd.to_datetime(df_fire['date'])
    df_fire.drop('date', axis=1, inplace=True)  # Drop the original 'date' column to avoid duplication

    # Remove duplicate dates, keeping the first occurrence
    # Note that weather info doesn't change for multiple entries of the same DATE
    # so this has no bearing on training the MODEL
    # multiple dates are kept so that we can map the fire locations
    df_weather_no_duplicates = df_weather.drop_duplicates(subset='DATE', keep='first')

    # Merge the datasets on the 'DATE' column
    combined_df = pd.merge(df_weather_no_duplicates, df_fire, on='DATE', how = 'inner')

    # Define features (X) and target (y)
    features = ['TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']
    X = combined_df[features]
    y = combined_df['Fire_exist']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create logistic regression model
    model = LogisticRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    # print("Accuracy:", accuracy_score(y_test, y_pred))
    # print(classification_report(y_test, y_pred))


    # Define the URL of the CSV file
    url = 'https://www.ncei.noaa.gov/data/global-hourly/access/2023/91190022516.csv'

    # Read the CSV file from the URL
    df = pd.read_csv(url, low_memory=False)

    # Rename the columns as required
    column_renames = {'WND': 'WDSP', 'DEW': 'DEWP', 'TMP': 'TEMP', 'AA1': 'PRCP'}
    df.rename(columns=column_renames, inplace=True)

    # Function to check for '9999' in the column
    def contains_9999(value):
        return '9999' in value


    # Convert columns to string to safely perform string operations
    df['WDSP'] = df['WDSP'].astype(str)
    df['DEWP'] = df['DEWP'].astype(str)
    df['TEMP'] = df['TEMP'].astype(str)
    df['PRCP'] = df['PRCP'].astype(str)

    # # Function to check and filter based on '9999' value
    # def filter_9999(value):
    #     parts = value.split(',')
    #     if len(parts) > 1 and parts[1].startswith('9999'):
    #         return False
    #     return True

    # Filter out rows with '9999' in the relevant columns
    df = df[~df['WDSP'].apply(contains_9999)]
    df = df[~df['DEWP'].apply(contains_9999)]
    df = df[~df['TEMP'].apply(contains_9999)]
    df = df[~df['PRCP'].apply(contains_9999)]


    # Convert the DATE column to datetime and truncate to just the date part
    df['DATE'] = pd.to_datetime(df['DATE']).dt.date

    # Extract the wind speed part from the 'WDSP' column
    # Assuming the wind speed (in tenths of meters per second) is the fourth element after splitting
    df['WDSP'] = df['WDSP'].str.split(',').str[3].str.extract(r'(\d+)').astype(float)

    # # Convert WDSP from meters per second to knots
    # 1 m/s = 1/0.51444 knots
    df['WDSP'] = df['WDSP'] / 5.1444

    # Convert columns to string to safely perform string operations
    df['DEWP'] = df['DEWP'].astype(str)

    # Extract the numeric part from the 'DEWP' column
    df['DEWP'] = df['DEWP'].str.split(',').str[0].str.extract(r'(\d+)').astype(float) / 10

    # Convert DEWP from Celsius to Fahrenheit
    df['DEWP'] = (df['DEWP'] * 9/5) + 32


    # Extract the numeric part from the 'TEMP' column without the sign
    df['TEMP'] = df['TEMP'].str.split(',').str[0].str.extract(r'(\d+)')

    # Convert TEMP from tenths of Celsius to Fahrenheit
    df['TEMP'] = df['TEMP'].astype(float) / 10  # Convert to Celsius
    df['TEMP'] = (df['TEMP'] * 9/5) + 32  # Convert to Fahrenheit

    # Convert columns to string to safely perform string operations
    df['PRCP'] = df['PRCP'].astype(str)

    # Extract the numeric part from the 'PRCP' column
    # Assuming the precipitation (in tenths of millimeters) is the second element after splitting
    df['PRCP'] = df['PRCP'].str.split(',').str[1].str.extract(r'(\d+)').astype(float)

    # Convert PRCP from tenths of millimeters to millimeters
    df['PRCP'] = df['PRCP'] / 100

    # Convert PRCP from millimeters to hundredths of inches
    df['PRCP'] = df['PRCP'] * 0.0393701

    # Select only the required columns
    columns_to_select = ['DATE', 'WDSP', 'STATION', 'DEWP', 'PRCP', 'TEMP']
    df = df[columns_to_select]

    # Filter out rows where any of the required columns are NaN
    df = df.dropna(subset=columns_to_select)

    # Select the last observation where all the required columns are not NaN
    last_valid_observation = df.iloc[-1:]

    # Display the last valid observation
    # print(last_valid_observation)

    # Filter out rows where any of the required columns are NaN
    df = df.dropna(subset=columns_to_select)

    # Select the last observation where all the required columns are not NaN
    # Use .copy() to explicitly make it a separate DataFrame
    last_valid_observation = df.iloc[-1:].copy()

    # Load the 'combined_fire_weather_data_pastyr.csv' data
    pastyr_df = df_weather

    # Ensure the 'DATE' column is in datetime format
    pastyr_df['DATE'] = pd.to_datetime(pastyr_df['DATE'])

    # Get the most recent date's 'past_day_fire_bin' value
    most_recent_fire_bin = pastyr_df.loc[pastyr_df['DATE'].idxmax(), 'past_day_fire_bin']

    # Add the 'past_day_fire_bin' column to the 'last_valid_observation' DataFrame
    last_valid_observation['past_day_fire_bin'] = most_recent_fire_bin

    # Display the combined data
    # print(last_valid_observation)

    # and then makes a prediction.

    required_features = ['TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']

    # Assuming 'last_valid_observation' already has these features, we proceed to make a prediction
    prediction_input = last_valid_observation[required_features]

    # Use the trained model to predict the probability
    predicted_probabilities = model.predict_proba(prediction_input)

    # The result will be in the form of an array of probabilities for each class ([probability of 0, probability of 1])
    # For binary classification, the probability of class 1 can be taken as the confidence level
    confidence_level = predicted_probabilities[0][1]

    # Output the prediction and confidence level
    predicted_fire_risk = model.predict(prediction_input)
    # print("Predicted Fire Risk for today:", predicted_fire_risk[0])
    # print("Confidence Level of the prediction:", confidence_level)

    required_features = ['TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']

    # Assuming 'last_valid_observation' already has these features, we proceed to make a prediction
    prediction_input = last_valid_observation[required_features]

    # Use the trained model to predict the probability
    predicted_probabilities = model.predict_proba(prediction_input)

    # The result will be in the form of an array of probabilities for each class ([probability of 0, probability of 1])
    # For binary classification, the probability of class 1 can be taken as the confidence level
    confidence_level = predicted_probabilities[0][1]

    # Output the prediction and confidence level
    predicted_fire_risk = model.predict(prediction_input)[0]

    # Create a DataFrame with date, predicted_fire_risk, and confidence level
    prediction_df = pd.DataFrame({
        'date': last_valid_observation['DATE'],
        'predicted_fire_risk': predicted_fire_risk,
        'confidence_level': confidence_level
    })

    # print(prediction_df)

    return prediction_df