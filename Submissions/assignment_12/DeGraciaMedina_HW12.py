# Homework #12: Hierarchical Data
# Author:  Xenia De Gracia Medina.
# Date: November 16, 2020.

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
import json
import urllib.request as req
import urllib
import seaborn as sn
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sn
import geopandas as gpd
import fiona
import shapely
from netCDF4 import Dataset

# %%
# Volumetric Soil Moisture from a NetCDF file
# Downloaded the data from https://psl.noaa.gov/cgi-bin/db_search/DBSearch.pl?Dataset=NCEP+Reanalysis+Daily+Averages&Variable=Volumetric+Soil+Moisture&group=0&submit=Search
# Net CDF file historical time series
data_path = os.path.join('../../../Geodatabases',
                         'Reanalysis_VolumetricSoilMoisture.nc')

# Read in the dataset as an x-array
dataset = xr.open_dataset(data_path)
# look at it
dataset

# We can inspect the metadata of the file like this:
metadata = dataset.attrs
metadata

# Focusing on just the Soil Moisture values
SoilMois = dataset['soilw']
SoilMois

# Now lets take a slice: Grabbing data for just one point
lat = dataset["soilw"]["lat"].values[0]
lon = dataset["soilw"]["lon"].values[0]
print("Long, Lat values:", lon, lat)
one_pointSM = dataset["soilw"].sel(lat=lat, lon=lon)
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
ax.set(title="Soil Moisture Time Series For a Single Lat / Lon Location")

plt.savefig("Soil_Moisture_Time_Series.png")

# Convert to dataframe
Soil_Moist_df = one_pointSM.to_dataframe()
Soil_Moist_W = Soil_Moist_df.resample("W-SUN").mean().round(2)

# Adding timezone = UTC to the flow data, to join the Mesowest data after
Soil_Moist_W.index = Soil_Moist_W.index.tz_localize(tz="UTC")

# FORECAST

# %%
# Flow Data from USGS
# Read the data, from the website, into a pandas dataframe.
Site = '09506000'
Start = '1989-01-01'
End = '2020-11-14'
url1 = 'https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&' \
       'site_no='+Site+'&referred_module=sw&period=&' \
       'begin_date='+Start+'&end_date='+End

print('The flow data is obtained  from: ', url1)
print()

data = pd.read_table(url1, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no', 'datetime', 'flow',
                            'code'],
                     parse_dates=['datetime'],
                     )


# Expand the dates to year, month, day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Xenia: NOTE that Now Mondays are represented by "dayofweek = 0" and Sundays \
# are represented by "dayofweek = 6"

# Aggregate flow values to daily and weekly
flow_daily = data.resample("D", on='datetime').min().round(2)
flow_weekly = data.resample("W-SUN", on='datetime').min().round(2)

# Adding timezone = UTC to the flow data, to join the Mesowest data after
flow_daily.index = flow_daily.index.tz_localize(tz="UTC")
flow_weekly.index = flow_weekly.index.tz_localize(tz="UTC")
print(flow_daily)
print()

# %%
# Building an autoregressive model
# Step 1: setup the arrays you will build your model on. Building it
# based on the lagged timeseries.

flow_daily['flow_tm1'] = flow_daily['flow'].shift(1)
flow_daily['flow_tm2'] = flow_daily['flow'].shift(2)

# Step 2: Taking train data from August to December 2019 because it was a dry \
# year too.
train = flow_daily.loc["2019-08-22":"2019-12-12"][['flow', 'flow_tm1',
                                                   'flow_tm2']]
# This shows the start and end of the training data.
print("The training data was taken from: ", train.index.min(), "  to  ",
      train.index.max())
print()

# Xenia: Taking data from last 3 years to test (3 years=1095 days)
test = flow_daily[-1095:][['flow', 'flow_tm1', 'flow_tm2']]

# Step 3: Fit a linear regression model using sklearn
x = train['flow_tm1'].values.reshape(-1, 1)
y = train['flow'].values
# Xenia: Shorten the steps to create the regression model
model = LinearRegression().fit(x, y)

# Look at the results
# r^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq, 2))

# Print the intercept and the slope
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# Step 4 Make a prediction with your model
# Predict the model response for a  given flow value
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1, 1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1, 1))

# alternatively you can calcualte this yourself like this:
# Xenia: y = b + m(x)
q_pred = model.intercept_ + (model.coef_ * train['flow_tm1'])
# Xenia: Printing the equation of the model
print('The AR model equation is:  y =', model.intercept_.round(2), '+',
      model.coef_.round(2), 'X')
# Xenia: Printing my prediction value. (I used thi mean value of the range.)
print('Prediction using equation from Linear Regression is:',
      np.round(q_pred.mean(), 2))

# %%
# you could also predict the q for just a single value like this
# Xenia: I used the minimum value of the last 3 WEEKS to forecast the coming
# week.
# Xenia: I made the same to predict the second week value, but using the
# minimun flow of the data from the LAST week only.
last_week_flow = flow_daily['flow'][-21].min()
last2_weeks_flow = flow_daily['flow'][-8].min()
prediction1stweek = model.intercept_ + model.coef_ * last_week_flow
prediction2ndweek = model.intercept_ + model.coef_ * last2_weeks_flow
# Xenia: Printing the equation of the model
print('First week prediction based on my AR model:',
      prediction1stweek.round(2))
print('Second week prediction based on my on my AR model:',
      prediction2ndweek.round(2))


# %%
# To compare with my initial method using just average of the last weeks:

# AVERAGE FIRST WEEK FORECAST
flow_mean1 = np.round(((data['flow'].tail(21)).mean()), 2)
print('The AVERAGE forecast for the FIRST week that comes is:', flow_mean1,
      'cf/s.')
print()

# AVERAGE  SECOND WEEK FORECAST
flow_mean2 = np.round(((data['flow'].tail(14)).mean()), 2)
print('The AVERAGE forecast for the SECOND week that comes is:', flow_mean2,
      'cf/s.')
print()

# %%
# PLOTS

# 1. Time series of flow values with the x axis range limited
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], label='full', color='grey')
ax.plot(train['flow'], 'r:', label='training', color='aqua', linestyle='-',
        alpha=0.50, dash_capstyle='round')
ax.plot(test['flow'], 'r:', label='testing', color='gold', linestyle='-',
        alpha=0.50, dash_capstyle='round')
ax.set(title="1. Testing, Training & Real Flow", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]", yscale='log',
       xlim=[datetime.date(1996, 8, 24), datetime.date(2021, 1, 1)])
ax.legend()
fig.set_size_inches(7, 5)
fig.savefig("1. Testing, Training & Real Flow.png")

# 2. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['flow'], color='purple', linewidth=2, label='observed')
ax.plot(train.index, q_pred_train, color='aqua', linestyle='-',
        label='simulated')
ax.set(title="2. Flow Simulation Done", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]", yscale='log')

plt.xticks(rotation=30)
ax.legend()
# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("2. Flow Simulation Done.png")

# 3. Scatter plot of t vs t-1 flow with log log axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='*',
           color='purple', label='obs')
ax.set(title="3. Autoregression Model", xlabel='flow t-1', ylabel='flow t',
       yscale='log', xscale='log')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model',
        color='aqua')
ax.legend()
# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("3. Autoregression Model.png")

# 4. Scatter plot of t vs t-1 flow with normal axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='*',
           color='purple', label='observations')
ax.set(title="4. Autoregression Model", xlabel='flow t-1', ylabel='flow t')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model',
        color='aqua')
ax.legend()
# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("4. Autoregression Model.png")

plt.show()

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


# Making PLOTS with Mesowest and USGS Data
end_date = '202011140000'

# Calling the function to get Precipitation and Temperature data from Mesowest
data_Meso, data_Meso_D, data_Meso_W = prec_temp_data(end_date)

# Printing my dataframe to know it
data_Meso_D

# %%
# Plots with Temperature & Precipitation
fig, ax = plt.subplots()
ax.plot(Soil_Moist_W['soilw'], 'r:', label='Soil Moisture',
        color='red', linestyle='-', alpha=1, linewidth=0.5)
ax.legend(loc=2)
ax.set(ylabel="Volumetric Soil Moisture (10-200 cm BGL)")
plt.xticks(rotation=30)
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot(flow_weekly['flow'], label='Streamflow', color='black',
         linewidth=0.5)
ax2.plot(data_Meso_W['Precipitation'], 'r:', label='Precipitation',
         color='aqua', linestyle='-', alpha=1, linewidth=0.7)
ax2.plot(data_Meso_W['Temperature'], 'r:', label='Temperature',
         color='mediumorchid', linestyle='-', alpha=1, linewidth=0.5)
ax2.legend()
ax2.set(title="2018-2021 data", xlabel="Date", ylabel="Weekly Avg values",
        yscale='log', xlim=[datetime.date(2018, 8, 24),
                            datetime.date(2021, 1, 1)])

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(7, 5)
fig.savefig("2018-2021_Data.png")

# %%
# Concatenate a single dataframe with all the time series
union = pd.concat([flow_weekly[['flow']], data_Meso_W[['Temperature']],
                   data_Meso_W[['Precipitation']],
                   Soil_Moist_W[['soilw']]], axis=1)

# %%
# Correlation Plot
corrMatrix = union.corr()
sn.heatmap(corrMatrix, annot=True, vmin=-1, vmax=1, center=0, cmap='PRGn')
plt.title("Correlation Matrix")
plt.show()
fig.set_size_inches(7, 5)
plt.savefig("Correlation_Matrix.png", bbox_inches='tight', pad_inches=0.0)

# %%
