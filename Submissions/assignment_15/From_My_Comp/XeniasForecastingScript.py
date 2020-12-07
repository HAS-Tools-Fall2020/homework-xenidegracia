# Homework #15: Computing resources
# Author of the code: Xenia De Gracia Medina.
# Date: December 07, 2020.

# %%
# 1. Update the necessary variables to make the code work
# NOTE Update this date
end_date = '2020-12-05'

# %%
# 2. Import the tools we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
import math
import json
import urllib.request as req
import urllib
import seaborn as sn
import xarray as xr
import seaborn as sn
import shapely
from shapely.geometry import Point

# %%
# 3. Getting the datasets to perform the modeling
# 3.1 Flow Data from USGS
# Read the data from the website, into a pandas dataframe.


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


# Calling the function to get the Flow data from USGS
data, flow_daily, flow_weekly = read_flow_data(end_date)

# %%
# 4. Autoregression modeling to obtain the flow forecast

# Step 1: setup the arrays you will build your model on. Building it
# based on the lagged timeseries.

flow_daily['flow_tm1'] = flow_daily['log_flow'].shift(1)
flow_daily['flow_tm2'] = flow_daily['log_flow'].shift(2)

# Step 2: Taking train data from August to December 2019 because it was a dry \
# year too.
train = flow_daily.loc["2019-08-22":"2019-12-12"][['log_flow', 'flow_tm1',
                                                   'flow_tm2']]
# This shows the start and end of the training data.
print("The training data was taken from: ", train.index.min(), "  to  ",
      train.index.max())
print()

# Xenia: Taking data from last 3 years to test (3 years=1095 days)
test = flow_daily[-1095:][['log_flow', 'flow_tm1', 'flow_tm2']]

# Step 3: Fit a linear regression model using sklearn
x = train['flow_tm1'].values.reshape(-1, 1)
y = train['log_flow'].values
# Xenia: Shorten the steps to create the regression model
model = LinearRegression().fit(x, y)

# Look at the results
# r^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq, 2))

# Print the intercept and the slope
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# %%
# Step 4 Make a prediction with your model
# Predict the model response for a  given flow value
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1, 1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1, 1))

# alternatively you can calcualte this yourself like this:
# Xenia: y = b + m(x)
q_pred = (model.intercept_) + (model.coef_ * train['flow_tm1'])
q_pred_W = q_pred.resample("W-SUN").min().round(2)
# Xenia: Printing the equation of the model
Equation = 'y = ' + str((model.intercept_).round(2)) + ' + ' + \
          str(model.coef_.round(2)) + 'X'
print('The AR model equation is: ', Equation)
# Xenia: Printing my prediction value. (I used the mean value of the range.)
print('Prediction using equation from Linear Regression is:',
      np.exp(q_pred_W))
print(type(q_pred_W))

# %%
# Prediction of the q for just a single value
# Xenia: I used the mean value of the last 3 WEEKS to forecast the coming
# week.
# Xenia: I made the same to predict the second week value, but using the
# minimun flow of the data from the LAST week only.
last_week_flow = flow_daily['log_flow'][-21].mean()
last2_weeks_flow = flow_daily['log_flow'][-8].min()
prediction1stweek = math.exp(model.intercept_ + (model.coef_ * last_week_flow))
prediction2ndweek = math.exp(model.intercept_ + (model.coef_ * last2_weeks_flow))
# Xenia: Printing the equation of the model
Message1 = 'First week prediction based on my AR model: '+ str(np.round(prediction1stweek,2)) + ' ft3/s'
print(Message1)
print()

Message2 = 'Second week prediction based on my on my AR model: ' + str(np.round(prediction2ndweek,2)) + ' ft3/s'
print(Message2)
print()

# %%
# To compare with my initial method using just average of the last weeks:

# AVERAGE FIRST WEEK FORECAST
flow_mean1 = np.round(((data['flow'].tail(21)).mean()), 2)
Message3 = 'The AVERAGE forecast for the FIRST week that comes is: ' + str(flow_mean1) + ' ft3/s'
print(Message3)
print()

# AVERAGE  SECOND WEEK FORECAST
flow_mean2 = np.round(((data['flow'].tail(14)).mean()), 2)
Message4 = 'The AVERAGE forecast for the SECOND week that comes is: ' + str(flow_mean2) + ' ft3/s'
print(Message4)
print()

# List of final message to print
MessageList = [Message1, Message2, Message3, Message4]
print(MessageList)

# Creating a dataframe from the MessageList
MessageDf = pd.DataFrame(MessageList)
MessageDf.to_csv('MessagePrinted.csv', index=False, header=False)

# %%
# 5. Visualization of the data through plots

# PLOTS

# 1. Time series of flow values with the x axis range limited
fig, ax = plt.subplots()
ax.plot(flow_weekly['log_flow'], label='full', color='grey')
ax.plot(test['log_flow'], 'r:', label='testing', color='purple', linestyle='-',
        alpha=0.50, dash_capstyle='round')
ax.plot(train['log_flow'], 'r:', label='training', color='aqua', linestyle='-',
        alpha=1, dash_capstyle='round')
ax.set(title="1. Testing, Training & Real Flow", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]", yscale='log',
       xlim=[datetime.date(1996, 8, 24), datetime.date(2021, 1, 1)])
ax.legend()
fig.set_size_inches(7, 5)
fig.savefig("1. Testing, Training & Real Flow.png")

# 2. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['log_flow'], color='purple', linewidth=2, label='observed')
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
ax.scatter(train['flow_tm1'], train['log_flow'], marker='.',
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
ax.scatter(train['flow_tm1'], train['log_flow'], marker='.',
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
