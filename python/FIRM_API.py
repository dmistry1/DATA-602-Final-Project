import pandas as pd

# 1.) Get the data for from FIRM API for the currect date.
# 2.) Parse out the data for just maui
# 3.) Return the data

# To do: 
# Pass in the current date and send that date to FIRM

MAP_KEY = '33c0bb32b80831ae1cb4bb94211611c8'

firm_api = 'https://firms.modaps.eosdis.nasa.gov//api/area/csv/33c0bb32b80831ae1cb4bb94211611c8/MODIS_NRT/world/1/2023-08-09'
df_firm = pd.read_csv(firm_api)

# Parsing out the latitude coordinates for the Maui island
df_firm = df_firm[(df_firm['latitude'] >= 20.500) & (df_firm['latitude'] <= 21.0000)]

df_firm = df_firm[(df_firm['longitude'] >= -156.5000) & (df_firm['longitude'] <= -156.0000)]

print (df_firm)