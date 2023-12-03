import folium
import getGoogleBucket
import pandas as pd

def getFireMap(date):
    data = getGoogleBucket.getData('combined_fire_weather_data_past_yr')
    df = pd.DataFrame(data)
    df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y')
    # Retrieve all rows with the date '8/9/2023'
    desired_date = pd.to_datetime(date, format='%m/%d/%Y')
    result_df = df[df['DATE'] == desired_date]
    red_points = result_df[['latitude', 'longitude']].to_numpy().tolist()
    map_maui = plot_points_on_map(red_points)
    return map_maui

def plot_points_on_map(red_points=None):
    # Coordinates for the center of Maui, Hawaii
    maui_center = [20.7984, -156.3319]

    # Create a map centered around Maui with the 'Stamen Terrain' tileset
    map_maui = folium.Map(location=maui_center, tiles='CartoDB dark_matter', zoom_start=10)

    # Add the second set of points in red, if provided
    if red_points:
        for lat, lon in red_points:
            folium.Circle(
                location=[lat, lon],
                radius=50,  # radius in meters
                color='red',
                fill=True,
                fill_color='red'
            ).add_to(map_maui)
    return map_maui

