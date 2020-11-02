# %%
import numpy as np
import pandas as pd
import json
import urllib.request as req
import urllib

# Creating the URL for the rest API
# Change demotoken to your token when running
mytoken = 'demotoken'
 
# This is the base url that will be the start our final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"
 
# Specific arguments for the data that we want
args = {
    'start': '199701010000',              # Must be this date for dataset
    'end': '202010240000',                # Update this on Sunday
    'obtimezone': 'UTC',
    'vars': 'air_temp',
    'stids': 'QVDA3',
    'units': 'temp|F',
    'token': mytoken}
apiString = urllib.parse.urlencode(args)
fullUrl = base_url + '?' + apiString
response = req.urlopen(fullUrl)
responseDict = json.loads(response.read())
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
airT = responseDict['STATION'][0]['OBSERVATIONS']['air_temp_set_1']
data2 = pd.DataFrame({'Temperature': airT}, index=pd.to_datetime(dateTime))
data_weekly = data2.resample('W').mean()

# %%
