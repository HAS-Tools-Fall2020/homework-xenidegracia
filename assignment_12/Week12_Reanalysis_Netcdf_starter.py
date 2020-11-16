# Homework #12: Hierarchical Data
# Author:  Xenia De Gracia Medina.
# Date: November 16, 2020.
# %%
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import fiona
import shapely
from netCDF4 import Dataset

# %%
# Precipitation
# Net CDF file historical time series
data_path = os.path.join('../../Geodatabases',
                         'Reanalysis_Precip.nc')

# Read in the dataset as an x-array
dataset = xr.open_dataset(data_path)
# look at it
dataset

# We can inspect the metadata of the file like this:
metadata = dataset.attrs
metadata

# Focusing on just the precip values
precip = dataset['prate']
precip

# Now lets take a slice: Grabbing data for just one point
lat = dataset["prate"]["lat"].values[0]
lon = dataset["prate"]["lon"].values[0]
print("Long, Lat values:", lon, lat)
one_point = dataset["prate"].sel(lat=lat, lon=lon)
one_point.shape

# use x-array to plot timeseries
one_point.plot.line()
precip_val = one_point.values

# Make a nicer timeseries plot
f, ax = plt.subplots(figsize=(12, 6))
one_point.plot.line(hue='lat',
                    marker="o",
                    ax=ax,
                    color="grey",
                    markerfacecolor="purple",
                    markeredgecolor="purple")
ax.set(title="Time Series For a Single Lat / Lon Location")

# Convert to dataframe
one_point_df = one_point.to_dataframe()


# %%
# Volumetric Soil Moisture
# Net CDF file historical time series
data_path2 = os.path.join('../../Geodatabases',
                          'Reanalysis_VolumetricSoilMoisture.nc')

# Read in the dataset as an x-array
dataset2 = xr.open_dataset(data_path2)
# look at it
dataset2

# We can inspect the metadata of the file like this:
metadata2 = dataset2.attrs
metadata2

# Focusing on just the Soil Moisture values
SoilMois = dataset2['soilw']
SoilMois

# Now lets take a slice: Grabbing data for just one point
lat = dataset2["soilw"]["lat"].values[0]
lon = dataset2["soilw"]["lon"].values[0]
print("Long, Lat values:", lon, lat)
one_pointSM = dataset2["soilw"].sel(lat=lat, lon=lon)
one_pointSM.shape

# use x-array to plot timeseries
one_pointSM.plot.line()
SoilMois_val = one_pointSM.values

# Make a nicer timeseries plot
f, ax = plt.subplots(figsize=(12, 6))
one_pointSM.plot.line(hue='lat',
                      marker="o",
                      ax=ax,
                      color="grey",
                      markerfacecolor="purple",
                      markeredgecolor="purple")
ax.set(title="Time Series For a Single Lat / Lon Location")

# Convert to dataframe
Soil_Moist_df = one_pointSM.to_dataframe()

# FORECAST
# %%
# Function for Mesowest Temperature & Precipitation data


def prec_temp_data(end_date):

    """ Obtaining Precipitation and Air Temperature from the Mesowest website.


    Parameters
    ----------
    end_date : updated date, to obtain the latest values.

    Returns
    ------
    data_Meso : dataframe with precipitation and temperature per hour
    data_Meso_D : dataframe with the means of precipitation and temperature \
                  per day
    data_Meso_W : dataframe with the means of precipitation and temperature \
                  per week

    """

    # This is the base url that will be the start our final url
    base_url = "http://api.mesowest.net/v2/stations/timeseries"

    # Specific arguments for the data that we want
    args = {
            'start': '199701010000',
            'end': end_date,
            'obtimezone': 'UTC',
            'vars': 'air_temp,precip_accum',
            'stids': 'QVDA3',
            'units': 'temp|C,precip|mm',
            'token': 'demotoken'}

    # Takes your arguments and paste them together into a string for the api
    apiString = urllib.parse.urlencode(args)

    # add the API string to the base_url
    fullUrl = base_url + '?' + apiString
    print('The Mesowest data is obtained from: ', fullUrl)

    # Request the data
    response = req.urlopen(fullUrl)

    # What we need to do now is read this data. The complete format of this:
    responseDict = json.loads(response.read())

    # Create a dictionary. Keys shows the main elements of it.
    responseDict.keys()

    # Get the data we want:
    dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
    airT = responseDict['STATION'][0]['OBSERVATIONS']['air_temp_set_1']
    precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_set_1']

    # Creating the pandas dataframe
    data_Meso = pd.DataFrame({'Temperature': airT, 'Precipitation': precip},
                             index=pd.to_datetime(dateTime))
    data_Meso_D = data_Meso.resample('D').mean().round(2)
    data_Meso_W = data_Meso.resample('W-SUN').mean().round(2)

    return data_Meso, data_Meso_D, data_Meso_W

# %%
# Adding timezone = UTC to the flow data, to join the Mesowest data after
daily_flow.index = daily_flow.index.tz_localize(tz="UTC")
weekly_flow_plot.index = weekly_flow_plot.index.tz_localize(tz="UTC")

# Concatenate a single dataframe with all the time series
union = pd.concat([weekly_flow_plot[['flow']], data_Meso_W[['Temperature']],
                   data_Meso_W[['Precipitation']]], axis=1)

# %%
# Correlation Plot
corrMatrix = union.corr()
sn.heatmap(corrMatrix, annot=True, vmin=-1, vmax=1, center=0, cmap='PRGn')
plt.title("Correlation_Matrix")
plt.show()
fig.set_size_inches(7, 5)
plt.savefig("Correlation_Matrix.png")

