import pandas as pd

# 1.) Get the data for from FIRM API for the currect date.
# 2.) Parse out the data for just maui
# 3.) Return the data

# To do: 
# Pass in the current date and send that date to FIRM

def getData(date):
    firm_api = "https://firms.modaps.eosdis.nasa.gov//api/area/csv/33c0bb32b80831ae1cb4bb94211611c8/MODIS_NRT/world/10/{}".format(date)
    print("rest",firm_api)
    df_firm = pd.read_csv(firm_api)

    # Removing column that are not needed  
    df_firm = df_firm.drop(['brightness', 'scan', 'track', 'acq_time', 'satellite', 
                            'instrument', 'confidence', 'version', 'bright_t31', 'daynight'], axis=1)

    # Reordering the data
    df_firm = df_firm[['acq_date', 'latitude', 'longitude', 'frp']]

    # Parsing out the latitude coordinates for the Maui island
    df_firm = df_firm[(df_firm['latitude'] >= 20.500) & (df_firm['latitude'] <= 21.0000)]

    # Parsing out the longitude coordinates for the Maui island
    df_firm = df_firm[(df_firm['longitude'] >= -154.5000) & (df_firm['longitude'] <= -157.0000)]
    print(df_firm)
    # Parsing out the FRP 
    df_firm = df_firm[(df_firm['frp'] > 100.00)]

    # Sorting latitude
    df_firm = df_firm.sort_values(by='latitude')
    df_firm.to_csv('./fireData.csv', index=False, mode='a', header=False)
