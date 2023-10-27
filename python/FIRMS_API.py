import pandas as pd

MAP_KEY = '33c0bb32b80831ae1cb4bb94211611c8'

# da_url = 'https://firms.modaps.eosdis.nasa.gov/api/data_availability/csv/' + MAP_KEY + '/all'
# df = pd.read_csv(da_url)
# print(df)


# VIIRS_SNPP_NRT data from Aug, 8, 2023
# latitude  longitude  bright_ti4  scan  track    acq_date  acq_time satellite instrument confidence version  bright_ti5   frp daynight
# ********************************************************
# latitude/longitude: Center of nominal 375 m fire pixel.
# bright_ti4 (Brightness temperature I-4): VIIRS I-4 channel brightness temperature of the fire pixel measured in Kelvin.
# scan: The algorithm produces approximately 375 m pixels at nadir. Scan and track reflect actual pixel size.
# track: The algorithm produces approximately 375 m pixels at nadir. Scan and track reflect actual pixel size.
# FRP(Fire Radiative Power): 
#           - depicts the pixel-integrated fire radiative power in megawatts (MW)
#           - detection algorithm was customized and tuned to optimize its response over small fires while balancing the occurrence of false alarms
#           - represents the rate of outgoing thermal radiative energy coming from a burning landscape fire
# usa_url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/33c0bb32b80831ae1cb4bb94211611c8/VIIRS_SNPP_NRT/world/1/2023-08-08'
# df_usa = pd.read_csv(usa_url)
# print('*************************** VIIRS_SNPP_NRT ***************************')
# print(df_usa)



# LANDSAT_NRT data from Aug, 8, 2023
# latitude  longitude  bright_ti4  scan  track    acq_date  acq_time satellite instrument confidence version  bright_ti5   frp daynight
# ********************************************************
# https://www.earthdata.nasa.gov/faq/firms-faq#ed-landsat-fires-attributes
# usa_url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/33c0bb32b80831ae1cb4bb94211611c8/LANDSAT_NRT/world/1/2023-08-08'
# df_usa = pd.read_csv(usa_url)
# print('*************************** LANDSAT_NRT ***************************')
# print(df_usa)


# MODIS_NRT data from Aug, 8, 2023
# latitude  longitude  bright_ti4  scan  track    acq_date  acq_time satellite instrument confidence version  bright_ti5   frp daynight
# ********************************************************
# https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/mcd14dl-nrt#ed-firms-attributes

# 20.80594,-156.27443,317.72,1.05,1.02,2023-08-08,1223,Aqua,MODIS,94,6.1NRT,292.02,17.25,N
# 20.80738,-156.28462,399.7,1.05,1.02,2023-08-08,1223,Aqua,MODIS,100,6.1NRT,306.84,271.21,N
# 20.80883,-156.29491,410.23,1.05,1.03,2023-08-08,1223,Aqua,MODIS,100,6.1NRT,306.25,345.34,N
# 20.81027,-156.30515,327.23,1.05,1.03,2023-08-08,1223,Aqua,MODIS,100,6.1NRT,293.99,27.27,N
# 20.8165,-156.2834,312.16,1.05,1.02,2023-08-08,1223,Aqua,MODIS,78,6.1NRT,292.21,11.63,N
# 20.81795,-156.29361,338.5,1.05,1.03,2023-08-08,1223,Aqua,MODIS,100,6.1NRT,295.21,43.94,N
# 20.06997,-155.858,371.12,1.57,1.23,2023-08-08,2057,Terra,MODIS,100,6.1NRT,305.44,219.22,D
# 20.07429,-155.86575,368,1.57,1.23,2023-08-08,2057,Terra,MODIS,100,6.1NRT,304.18,195.29,D
# 20.07856,-155.84259,320.74,1.57,1.24,2023-08-08,2057,Terra,MODIS,30,6.1NRT,307,15.61,D
# 20.08278,-155.85023,342.98,1.57,1.23,2023-08-08,2057,Terra,MODIS,69,6.1NRT,309.8,73.97,D
# 20.09611,-155.86247,321.55,1.57,1.23,2023-08-08,2057,Terra,MODIS,0,6.1NRT,308.78,19.33,D
# 20.80798,-156.29138,339.14,1.42,1.18,2023-08-08,2057,Terra,MODIS,86,6.1NRT,303.61,57.82,D
# 20.81008,-156.30362,352.08,1.42,1.18,2023-08-08,2057,Terra,MODIS,96,6.1NRT,309.35,96.93,D
# 20.81223,-156.31613,322.09,1.42,1.18,2023-08-08,2057,Terra,MODIS,52,6.1NRT,305.75,15.31,D
# 20.82039,-156.30136,325.91,1.42,1.18,2023-08-08,2057,Terra,MODIS,63,6.1NRT,305.56,26.51,D

usa_url = 'https://firms.modaps.eosdis.nasa.gov//api/area/csv/33c0bb32b80831ae1cb4bb94211611c8/MODIS_NRT/world/1/2023-08-08'
df_usa = pd.read_csv(usa_url)
print('*************************** MODIS_NRT ***************************')
df_usa = pd.read_csv(usa_url)

print(df_usa)

# 20.78356,-156.42429,341.08,1.04,1.02,2023-08-09,2358,Aqua,MODIS,64,6.1NRT,317.57,20.19,D
# 20.78806,-156.39455,343.39,1.04,1.02,2023-08-09,2358,Aqua,MODIS,49,6.1NRT,320.37,22.97,D
# 20.78955,-156.38464,342.55,1.04,1.02,2023-08-09,2358,Aqua,MODIS,45,6.1NRT,318.49,24.38,D
# 20.79105,-156.37476,344.74,1.04,1.02,2023-08-09,2358,Aqua,MODIS,86,6.1NRT,316.77,32.67,D
# 20.79987,-156.43291,333.04,1.04,1.02,2023-08-09,2358,Aqua,MODIS,85,6.1NRT,312.69,16.1,D
# 20.80292,-156.4131,350.99,1.04,1.02,2023-08-09,2358,Aqua,MODIS,96,6.1NRT,316.08,50.4,D
# 20.80444,-156.40324,341.23,1.04,1.02,2023-08-09,2358,Aqua,MODIS,91,6.1NRT,313.61,29.97,D
# 20.80451,-156.28539,356.96,1.04,1.02,2023-08-09,2358,Aqua,MODIS,98,6.1NRT,306.18,70.93,D
# 20.80596,-156.39337,334.12,1.04,1.02,2023-08-09,2358,Aqua,MODIS,86,6.1NRT,312.24,19.34,D
# 20.8271,-156.31593,328.59,1.04,1.02,2023-08-09,2358,Aqua,MODIS,47,6.1NRT,308.72,16.62,D
# 20.7669,-156.32317,324.86,2.11,1.41,2023-08-09,750,Terra,MODIS,100,6.1NRT,292.86,68.35,N
# 20.76847,-156.33,311.08,2.11,1.41,2023-08-09,750,Terra,MODIS,62,6.1NRT,292.81,29.57,N
# 20.77088,-156.30083,334.93,2.1,1.41,2023-08-09,750,Terra,MODIS,100,6.1NRT,291.71,107.89,N
# 20.77257,-156.30795,341.66,2.1,1.41,2023-08-09,750,Terra,MODIS,100,6.1NRT,294.45,138.68,N
# 20.7764,-156.41464,336.69,2.14,1.42,2023-08-09,750,Terra,MODIS,100,6.1NRT,297.9,110.45,N
# 20.77744,-156.42061,320.18,2.14,1.42,2023-08-09,750,Terra,MODIS,100,6.1NRT,296.87,48.74,N
# 20.77905,-156.3269,336.06,2.11,1.41,2023-08-09,750,Terra,MODIS,100,6.1NRT,293.96,108.4,N
# 20.78008,-156.39378,381.98,2.13,1.42,2023-08-09,750,Terra,MODIS,100,6.1NRT,305.85,482.47,N
# 20.78064,-156.33356,319.3,2.11,1.41,2023-08-09,750,Terra,MODIS,97,6.1NRT,292.72,46.88,N
# 20.78126,-156.39986,375.61,2.13,1.42,2023-08-09,750,Terra,MODIS,100,6.1NRT,304.24,406.28,N
# 20.78294,-156.30489,315.38,2.1,1.41,2023-08-09,750,Terra,MODIS,52,6.1NRT,291.3,39.37,N
# 20.78377,-156.37285,361.22,2.12,1.42,2023-08-09,750,Terra,MODIS,100,6.1NRT,301.84,264.9,N
# 20.78466,-156.31177,321.55,2.1,1.41,2023-08-09,750,Terra,MODIS,96,6.1NRT,292.07,55.17,N
# 20.7851,-156.37904,375.35,2.12,1.42,2023-08-09,750,Terra,MODIS,100,6.1NRT,305.26,402.19,N
# 20.78897,-156.358,315.3,2.12,1.41,2023-08-09,750,Terra,MODIS,88,6.1NRT,295.36,35.68,N
# 20.79364,-156.40268,345.46,2.13,1.42,2023-08-09,750,Terra,MODIS,100,6.1NRT,298.04,155.32,N
# 20.79741,-156.38206,362.5,2.12,1.42,2023-08-09,750,Terra,MODIS,100,6.1NRT,299.01,276.12,N
# 20.79893,-156.28665,309.06,2.09,1.41,2023-08-09,750,Terra,MODIS,13,6.1NRT,289.34,27.36,N
# 20.80077,-156.29378,306.91,2.09,1.41,2023-08-09,750,Terra,MODIS,25,6.1NRT,290.26,22.89,N
# 20.86201,-156.67784,410.64,2.23,1.45,2023-08-09,750,Terra,MODIS,100,6.1NRT,310.3,1031.53,N
# 20.87468,-156.68048,364.29,2.23,1.45,2023-08-09,750,Terra,MODIS,100,6.1NRT,304.67,307.31,N
# 20.87872,-156.65823,311.8,2.22,1.44,2023-08-09,750,Terra,MODIS,48,6.1NRT,297.96,34.21,N
# 20.88687,-156.68843,338.85,2.23,1.45,2023-08-09,750,Terra,MODIS,100,6.1NRT,299.54,126.96,N
# 20.89099,-156.66656,326.5,2.22,1.44,2023-08-09,750,Terra,MODIS,100,6.1NRT,297.7,78.12,N
# 20.89141,-156.6606,307.21,2.22,1.44,2023-08-09,750,Terra,MODIS,33,6.1NRT,296.47,26,N
# 20.76995,-156.29987,322.68,3.25,1.7,2023-08-09,1304,Aqua,MODIS,100,6.1NRT,288.25,121.87,N
# 20.77257,-156.30524,321.42,3.25,1.7,2023-08-09,1304,Aqua,MODIS,100,6.1NRT,289.15,113.08,N
# 20.78278,-156.35643,306.6,3.21,1.7,2023-08-09,1304,Aqua,MODIS,32,6.1NRT,291.03,38.85,N
# 20.78586,-156.37709,323.26,3.19,1.69,2023-08-09,1304,Aqua,MODIS,100,6.1NRT,293.29,109.68,N
# 20.78817,-156.38351,328.58,3.19,1.69,2023-08-09,1304,Aqua,MODIS,100,6.1NRT,294.58,144.23,N
# 20.79152,-156.4046,327.81,3.18,1.69,2023-08-09,1304,Aqua,MODIS,100,6.1NRT,294.92,134.7,N
# 20.79367,-156.41118,326.32,3.18,1.69,2023-08-09,1304,Aqua,MODIS,100,6.1NRT,294.94,124.5,N
# 20.80065,-156.37352,313.48,3.19,1.69,2023-08-09,1304,Aqua,MODIS,82,6.1NRT,293.03,62.19,N
# 20.80295,-156.37987,311.4,3.19,1.69,2023-08-09,1304,Aqua,MODIS,73,6.1NRT,293.3,53.04,N
# 20.80629,-156.40106,313.69,3.18,1.69,2023-08-09,1304,Aqua,MODIS,83,6.1NRT,294.11,61.68,N
# 20.8591,-156.66551,331.3,3.03,1.66,2023-08-09,1304,Aqua,MODIS,100,6.1NRT,295.9,146.84,N
# 20.87348,-156.6564,309.95,3.03,1.66,2023-08-09,1304,Aqua,MODIS,68,6.1NRT,295.08,45.55,N
# 20.87376,-156.66299,316.59,3.03,1.66,2023-08-09,1304,Aqua,MODIS,54,6.1NRT,295.99,65.48,N
# 20.8788,-156.68275,321.89,3.02,1.65,2023-08-09,1304,Aqua,MODIS,100,6.1NRT,295.98,87.48,N
# 20.88834,-156.6548,315.08,3.03,1.66,2023-08-09,1304,Aqua,MODIS,77,6.1NRT,294.6,63.16,N

usa_url = 'https://firms.modaps.eosdis.nasa.gov//api/area/csv/33c0bb32b80831ae1cb4bb94211611c8/MODIS_NRT/world/1/2023-08-09'
df_usa = pd.read_csv(usa_url)
print('*************************** MODIS_NRT ***************************')
df_usa = pd.read_csv(usa_url)

print(df_usa)

# 20.7992,-156.28459,312.24,1.38,1.16,2023-08-10,833,Terra,MODIS,78,6.1NRT,288.48,20.87,N