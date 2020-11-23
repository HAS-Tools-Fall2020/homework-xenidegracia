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
import contextily as ctx
import shapely
from shapely.geometry import Point
from netCDF4 import Dataset

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
# Function to read the data from the USGS website, into a pandas dataframe.
def read_flow_data(end_date):

    """ Obtaining flow values from the USGS website.


    Parameters
    ----------
    end_date : updated date, to obtain the latest values.

    Returns
    ------
    data : dataframe with flow values
    flow_daily : dataframe with the datetime index and daily values
    flow_weekly : dataframe with the datetime index, resample to weekly values

    """

    Site = '09506000'
    Start = '1989-01-01'
    End = end_date
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

    # Xenia: NOTE that Now Mondays are represented by "dayofweek = 0" and \
    # Sundays # are represented by "dayofweek = 6"

    # Aggregate datetime index to daily flow values and resample to weekly
    flow_daily = data.resample("D", on='datetime').min().round(2)
    flow_daily.insert(2, 'log_flow', np.log(flow_daily['flow']), True)
    flow_weekly = flow_daily.resample("W-SUN", on='datetime').min().round(2)

    # Adding timezone = UTC to the flow data, to join the Mesowest data after
    flow_daily.index = flow_daily.index.tz_localize(tz="UTC")
    flow_weekly.index = flow_weekly.index.tz_localize(tz="UTC")
    print(flow_daily)
    print()

    return data, flow_daily, flow_weekly


# %%

# %%
