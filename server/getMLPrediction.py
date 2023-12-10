import getGoogleBucket
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier

def getPrediction():
    # Loads both of the csv from google cloud storage
    df_weather = getGoogleBucket.getData('combined_fire_weather_data_past_yr')
    df_fire = getGoogleBucket.getData('fire_weather_dates_ml_binary')

    # Make a copy and convert 'DATE' columns to datetime
    df_weather = df_weather.copy()
    df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])

    df_fire = df_fire.copy()
    df_fire['DATE'] = pd.to_datetime(df_fire['date'])
    df_fire.drop('date', axis=1, inplace=True)

    # Select relevant columns
    columns_to_use = ['DATE', 'TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']
    df_weather = df_weather[columns_to_use]

    # Remove duplicate dates
    df_weather_no_duplicates = df_weather.drop_duplicates(subset='DATE', keep='first')

    # Merge the datasets on the 'DATE' column
    combined_df = pd.merge(df_weather_no_duplicates, df_fire, on='DATE', how='inner')

    # Define features (X) and target (y)
    features = ['TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']
    X = combined_df[features]
    y = combined_df['Fire_exist']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Apply SMOTE to balance the dataset
    smote = SMOTE()
    # X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    # Initialize XGBoost model with the best parameters
    best_params = {'colsample_bytree': 0.6, 'gamma': 0.5, 'max_depth': 4, 'min_child_weight': 1, 'subsample': 1.0}
    model = XGBClassifier(**best_params)

    # Train the model with the best parameters on the balanced dataset
    model.fit(X_train_smote, y_train_smote)

    
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

    # Filter out rows where any of the required columns are NaN
    df = df.dropna(subset=columns_to_select)

    # Select the last observation where all the required columns are not NaN
    # Use .copy() to explicitly make it a separate DataFrame
    last_valid_observation = df.iloc[-1:].copy()

    # Load the 'combined_fire_weather_data_pastyr.csv' data
    # df_weather = pd.read_csv('/content/drive/My Drive/combined_fire_weather_data_pastyr.csv')

    # Ensure the 'DATE' column is in datetime format
    df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])

    # Get the most recent date's 'past_day_fire_bin' value
    most_recent_fire_bin = df_weather.loc[df_weather['DATE'].idxmax(), 'past_day_fire_bin']

    # Add the 'past_day_fire_bin' column to the 'last_valid_observation' DataFrame
    last_valid_observation['past_day_fire_bin'] = most_recent_fire_bin

    # Assuming 'last_valid_observation' is a DataFrame with a single row
    # List of features used during the training of the XGBoost model
    features = ['TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']

    # Select only the required features from last_valid_observation
    prediction_input_df = last_valid_observation[features]

    # Use the trained XGBoost model to make a prediction
    # Note: Replace 'model' with your actual trained XGBoost model variable
    predicted_fire_risk = model.predict(prediction_input_df)

    # Since the output will be in an array, extract the single prediction value
    predicted_fire_risk = predicted_fire_risk[0]

    # Get the predicted probabilities for each class
    predicted_probabilities = model.predict_proba(prediction_input_df)
    # Extract the probability of the positive class (assuming it is the second column)
    confidence_level = predicted_probabilities[0][1]

    # Create a DataFrame with date, predicted_fire_risk, and confidence level
    prediction_df = pd.DataFrame({
        'date': last_valid_observation['DATE'],
        'predicted_fire_risk': [predicted_fire_risk],
        'confidence_level': [confidence_level]
    })

    return prediction_df