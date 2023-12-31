import pandas as pd
import folium
import branca.colormap as cm
from geopy.distance import geodesic


def getFireMap(prediction_df):
    # Directly access the values in the single row of prediction_df
    date = prediction_df['date'].iloc[0]
    predicted_fire_risk = prediction_df['predicted_fire_risk'].iloc[0]
    confidence_level = prediction_df['confidence_level'].iloc[0]

    # Fetch fire data for the specific date
    df_fires = get_fire_data(date)
    maui_center = [20.7984, -156.3319]
    maui_map = folium.Map(location=maui_center, tiles='CartoDB dark_matter', zoom_start=10)

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

    # Save map for each date
    # maui_map.save(f'maui_fire_map_with_predictions_{date}.html')
    return maui_map
    
# Function to get fire data from FIRMS API for a specific date and parse out the data for just Maui
def get_fire_data(date):
    firm_api = f"https://firms.modaps.eosdis.nasa.gov//api/area/csv/33c0bb32b80831ae1cb4bb94211611c8/MODIS_NRT/world/1/{date}"
    df_firm = pd.read_csv(firm_api)
    df_firm = df_firm[['acq_date', 'latitude', 'longitude', 'frp']]
    df_firm = df_firm[(df_firm['latitude'] >= 20.500) & (df_firm['latitude'] <= 21.0000)]
    df_firm = df_firm[(df_firm['longitude'] >= -156.5000) & (df_firm['longitude'] <= -156.0000)]
    df_firm = df_firm[df_firm['frp'] > 0]
    df_firm = df_firm.sort_values(by='latitude')
    return df_firm

# Function to determine circle size based on prediction score
def get_circle_radius(prediction_score):
    # This is a simple linear scaling. You can adjust the scaling factor as needed.
    return prediction_score * 10000000  # for example, 10 meters per score unit

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
