import folium
import getGoogleBucket
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from geopy.distance import geodesic
import branca.colormap as cm

# Function to create a map with fire locations marked as squares
def create_fire_map(date):
    ml_predictions = get_old_prediction(date)
    df_fires = get_fire_data(date)
    maui_center = [20.7984, -156.3319]
    maui_map = folium.Map(location=maui_center, tiles='CartoDB dark_matter', zoom_start=10)
    # Directly access the values in the single row of prediction_df
    date = ml_predictions['date'].iloc[0]
    predicted_fire_risk = ml_predictions['predicted_fire_risk'].iloc[0]
    confidence_level = ml_predictions['confidence_level'].iloc[0]

    # Check if there are fire spots
    if not df_fires.empty:
        # Create a red color scale for the FRP values
        max_frp = df_fires['frp'].max()
        min_frp = df_fires['frp'].min()

        # Define a color scale from light red to dark red using hexadecimal colors
        colormap = cm.LinearColormap(['#ffcccc', '#ff0000'], vmin=min_frp, vmax=max_frp)

        for _, row in df_fires.iterrows():
            corners = get_square_corners(row['latitude'], row['longitude'])
            color = colormap(row['frp'])
            folium.Polygon(
                locations=corners,
                color=color,
                fill=True,
                fill_color=color
            ).add_to(maui_map)

        # Add the color scale legend to the map
        colormap.caption = 'Fire Radiative Power (FRP)'
        maui_map.add_child(colormap)
    else:
        # Add a message to the map indicating no fire spots
        folium.Marker(
            location=[20.7984, -156.3319],
            popup="No fire locations on this date",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(maui_map)

    # Extract the prediction score for the given date
    prediction_score = ml_predictions[ml_predictions['date'] == date]['confidence_level'].max()

    # Plot the prediction as a circle
    circle_color = 'orange' if predicted_fire_risk > 0 else 'blue'
    circle_radius = get_circle_radius(confidence_level)
    folium.Circle(
        location=maui_center,  # Adjust location if necessary
        radius=circle_radius,
        color=circle_color,
        fill=True,
        fill_color=circle_color
    ).add_to(maui_map)

    maui_map.save(f'maui_fire_map_with_predictions_{date}.html')
    return maui_map

# Function to determine circle size based on prediction score
def get_circle_radius(prediction_score, min_radius=1000, max_radius=8500):
    # Scale the prediction score (0 to 1) to the radius range (min_radius to max_radius)
    scaled_radius = prediction_score * (max_radius - min_radius) + min_radius

    # Ensure the radius does not go below the minimum or above the maximum
    return max(min(scaled_radius, max_radius), min_radius)

# Function to get fire data from FIRMS API for a specific date and parse out the data for just Maui
def get_fire_data(date):
    data = getGoogleBucket.getData('combined_fire_weather_data_past_yr')	
    df = pd.DataFrame(data)	
    df['DATE'] = pd.to_datetime(df['DATE'])	
    # Retrieve all rows with the date '8/9/2023'	
    desired_date = pd.to_datetime(date)	
    result_df = df[df['DATE'] == desired_date]	
    return result_df

# Function to calculate square corners around a point
def get_square_corners(lat, lon, distance_km=0.5):
    # Calculate the four corners of a square centered at (lat, lon)
    # distance_km is the half-side of the square, defaulting to 0.5 km for a 1km x 1km square
    center = (lat, lon)
    north = geodesic(kilometers=distance_km).destination(center, bearing=0)
    east = geodesic(kilometers=distance_km).destination(center, bearing=90)
    south = geodesic(kilometers=distance_km).destination(center, bearing=180)
    west = geodesic(kilometers=distance_km).destination(center, bearing=270)

    ne = (north.latitude, east.longitude)
    se = (south.latitude, east.longitude)
    sw = (south.latitude, west.longitude)
    nw = (north.latitude, west.longitude)

    return [ne, se, sw, nw, ne]  # Return coordinates to form a closed square


def get_old_prediction(date):
  df = getGoogleBucket.getData('combined_fire_weather_data_past_yr')
  # df = pd.read_csv(df_weather)
  # print('df', df)
  df['DATE'] = pd.to_datetime(df['DATE'])
  # Format the input date string to a datetime object
  input_date = pd.to_datetime(date)
  # Filter the DataFrame to only include rows with the specified date
  df_filtered = df[df['DATE'] == input_date]

  required_features = ['TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']

  prediction_input = df_filtered[required_features]

  # Use the trained model to predict the probability
  model = tain_model_on_date(date)

  predicted_probabilities = model.predict_proba(prediction_input)
  confidence_level = predicted_probabilities[0][1]
  predicted_fire_risk = model.predict(prediction_input)[0]

  prediction_df = pd.DataFrame({
      'date': df_filtered['DATE'],
      'predicted_fire_risk': predicted_fire_risk,
      'confidence_level': confidence_level
  })

  return prediction_df

def tain_model_on_date(date):
    # Load the datasets
    df_weather = getGoogleBucket.getData('combined_fire_weather_data_past_yr')
    df_fire = getGoogleBucket.getData('fire_weather_dates_ml_binary')

    # Convert 'DATE' columns to datetime
    df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])
    df_fire['DATE'] = pd.to_datetime(df_fire['date'])
    df_fire.drop('date', axis=1, inplace=True)

    # Filter the dataframes to remove dates beyond the given date
    cutoff_date = pd.to_datetime(date)
    df_weather = df_weather[df_weather['DATE'] <= cutoff_date]
    df_fire = df_fire[df_fire['DATE'] <= cutoff_date]

    # Make sure to include the date 07/05/2023
    crucial_date = pd.to_datetime('2023-07-05')
    crucial_data = df_weather[df_weather['DATE'] == crucial_date]
    crucial_fire_data = df_fire[df_fire['DATE'] == crucial_date]

    # Exclude the crucial date from the rest of the dataset for random splitting
    df_weather = df_weather[df_weather['DATE'] != crucial_date]
    df_fire = df_fire[df_fire['DATE'] != crucial_date]


    # Continue with your existing logic...
    columns_to_use = ['DATE', 'TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']
    df_weather = df_weather[columns_to_use]
    df_weather_no_duplicates = df_weather.drop_duplicates(subset='DATE', keep='first')
    combined_rest = pd.merge(df_weather_no_duplicates, df_fire, on='DATE', how='inner')

    features = ['TEMP', 'past_day_fire_bin', 'WDSP', 'DEWP', 'PRCP']

    # Define features (X) and target (y) for the rest of the data
    X_rest = combined_rest[features]
    y_rest = combined_rest['Fire_exist']

    # Define features and target for the crucial date
    X_crucial = crucial_data[features]
    y_crucial = crucial_fire_data['Fire_exist']


    # Check class distribution in crucial data
    # Combine crucial data with the rest of the data
    X_combined = pd.concat([X_crucial, X_rest], ignore_index=True)
    y_combined = pd.concat([y_crucial, y_rest], ignore_index=True)

    # Check combined class distribution
    #print("Combined data class distribution:\n", y_combined.value_counts())

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.2, random_state=42)

    # Create logistic regression model
    model = LogisticRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division = 0))

    return model
