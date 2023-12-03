import folium

def plot_points_on_map(orange_points, red_points=None):
    # Coordinates for the center of Maui, Hawaii
    maui_center = [20.7984, -156.3319]

    # Create a map centered around Maui with the 'Stamen Terrain' tileset
    map_maui = folium.Map(location=maui_center, tiles='CartoDB dark_matter', zoom_start=10)

    # Add points to the map using Circle
    for lat, lon in orange_points:
        folium.Circle(
            location=[lat, lon],
            radius=50,  # radius in meters
            color='orange',
            fill=True,
            fill_color='orange'
        ).add_to(map_maui)

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

    # Display the map
    return map_maui


orange_points = [
[20.7984, -156.3319],
[20.9001, -156.4370],
[20.8893, -156.4729],
[20.7986, -156.2525],
[20.8558, -156.3419],
[20.7211, -156.4474],
[20.6906, -156.4394],
[20.8843, -156.6819],
[20.7598, -156.4569],
[20.7982, -156.5145],
[20.8383, -156.3417],
[20.9162, -156.3826],
[20.7808, -156.3192],
[20.8583, -156.6933],
[20.6932, -156.4397],
[20.8849, -156.4637],
[20.7644, -156.4450],
[20.8087, -156.3333],
[20.7376, -156.4456],
[20.9219, -156.3794]
]
red_points = [
[20.7987, -156.3313],
[20.9006, -156.4372],
[20.8895, -156.4721],
[20.7984, -156.2520],
[20.8553, -156.3411],
[20.7212, -156.4472],
[20.6901, -156.4393],
[20.8840, -156.6814],
[20.7599, -156.4565],
[20.7988, -156.5143],
[20.8387, -156.3419],
[20.9166, -156.3821],
[20.7805, -156.3199],
[20.8584, -156.6938],
[20.6933, -156.4393],
[20.8842, -156.4636],
[20.7641, -156.4452],
[20.8080, -156.3336],
[20.7379, -156.4455],
[20.9218, -156.3792]
]

map_maui = plot_points_on_map(orange_points, red_points)
map_maui.save("./maui_map.html")  # Saves the map to an HTML file
print(map_maui)
# return jsonpickle.encode(map_maui)

