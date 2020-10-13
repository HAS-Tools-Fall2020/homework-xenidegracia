# Week 7: Coding cleaning and interpretation
# AR model and plot it

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime

# Note: you may need to do pip install for sklearn

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data

# ACTION REQUIRED: change the name of the file with the current number of \
# the week
filename = 'streamflow_week7.txt'

# ACTION REQUIRED: Please make sure the 'filepath' variable work in your \
# device.

# The variable "filepath" will automatically join the address of your data \
# and the document.
filepath = os.path.join('..\..\data', filename)
print('The current work directory is:', os.getcwd())
print()
print('The data is storaged at:', filepath)
print()

# This shows if the path exists or not, to check if there is any problem
# finding the data. "True" means it's ok. "False" means there is a problem.
print('Is everything ok with the path to start working now?')
os.path.exists(filepath)

# %%
# Read the data into a pandas dataframe
data = pd.read_table(filepath, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no', 'datetime', 'flow',
                            'code'],
                     parse_dates=['datetime']
                     )

# Expand the dates to year, month, day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Xenia: Note that Now Mondays are represented by "dayofweek = 0" and Sundays \
# are represented by "dayofweek = 6"

# Aggregate flow values to weekly.
# Xenia: Here I changed from mean function, to min function, becauase I want \
# to consider just the minimun values of each week.
flow_weekly = data.resample("W", on='datetime').min().round(2)


# %%
# Building an autoregressive model

# Step 1: setup the arrays you will build your model on
# This is an autoregressive model so we will be building it based on the \
# Lagged timeseries
flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)

# Step 2 - pick what portion of the time series you want to use as training \
# data
# Here I'm grabbing the first 800 weeks
# Note1 - dropping the first two weeks since they wont have lagged data \
# to go with them

# Xenia: Taking train data from 1994 to 2004 because... you only live once?

# Xenia: Converting the training years and to weeks.
# FUNCTION to convert the specific training years, to weeks.


def StudyYears_to_weeks(number_of_year):
    """ It converts the quantity of years, to weeks and rounded to two
    decimals.

    Parameters
    ----------
    number_of_year : int

    Returns
    ------
    conversion1 : str, int
    """

    conversion1 = round(((number_of_year - 1989)*52), 2)

    return conversion1


start_train_week = StudyYears_to_weeks(1996)
final_train_week = StudyYears_to_weeks(2004)


train = flow_weekly[start_train_week:final_train_week][['flow', 'flow_tm1',
                                                        'flow_tm2']]
print("From ", train.index.min(), " to ", train.index.max())
print()

# Xenia: Taking test data from 3 last years. Convert years to weeks through
# the function below.
# FUNCTION to convert the quantity of testing years, to weeks.


def convert_years_to_weeks(years_to_test):
    """ It converts the quantity of testing years, to weeks.

    Parameters
    ----------
    years_to_test : str, int

    Returns
    ------
    conversion2 : str, int
    """

    conversion2 = (years_to_test * 52)

    return conversion2


years_to_weeks = convert_years_to_weeks(3)
print('The quantity of weeks to test the model is:', years_to_weeks)
print()

# Finally obtaining the train test value after using the function.
test = flow_weekly[-years_to_weeks:][['flow', 'flow_tm1', 'flow_tm2']]

# Step 3: Fit a linear regression model using sklearn
x = train['flow_tm1'].values.reshape(-1, 1)
y = train['flow'].values

# Xenia: Shorten the steps to create the regression model
model = LinearRegression().fit(x, y)

# Look at the results
# R^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq, 2))
print()

# Print the intercept and the slope
print('intercept:', np.round(model.intercept_, 2))
print()
print('slope:', np.round(model.coef_, 2))
print()

# Step 4 Make a prediction with your model
# Predict the model response for a given flow value
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1, 1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1, 1))

# Alternatively you can calcualte this yourself like this:
# Xenia: y = b + m(x)
q_pred = model.intercept_ + (model.coef_ * train['flow_tm1'])

# Xenia: Printing the final equation of the model
print('The AR model equation is:  y =', model.intercept_.round(2), '+',
      model.coef_.round(2), 'X')
print()

# Xenia: Printing the prediction value. I used the minimun value of the range.
# Xenia: Please use this value for the 1st week Regression based Forecast.
print('First Week prediction using equation from Linear Regression is:',
      q_pred.min().round(2))
print('Thanks for NOT using this value for the 1st week Regression based Forecast')

print()

# %%
# You could also predict the q for just a single value like this.

# Xenia: I used the minimum value of the last 4 WEEKS to forecast the \
# coming week.
# Xenia: Please USE this value for AR prediction.
last_4weeks_flow = flow_weekly['flow'][-4].min()
prediction_1stWeek = model.intercept_ + model.coef_ * last_4weeks_flow
print('First week prediction using AR but based just on my 4 last weeks\
      average value is:', prediction_1stWeek.round(2))
print('Please Use this value for the 1st week Regression based Forecast')
print()

# Xenia: I made the same to predict the second week value, but using the \
# minimun flow from the LAST 3 weeks only.
# Xenia: Please USE this value for AR prediction.
last_3weeks_flow = flow_weekly['flow'][-3].min()
prediction_2ndWeek = model.intercept_ + model.coef_ * last_3weeks_flow
print('Second week prediction using AR but based just on my 3 last weeks \
      average value is:', prediction_2ndWeek.round(2))
print('Please Use this value for the 2nd week Regression based Forecast')
print()

# %%
# My initial forecast method is using just average of the last weeks:

# AVERAGE FIRST WEEK FORECAST (Please choose this for the 1st week CSV entry).
flow_mean1 = round(((data['flow'].tail(21)).mean()),2)  #.round(2)
print('The AVERAGE forecast for the FIRST week that comes is:', flow_mean1,
      'cf/s.')
print('Use this value for the 1st week CSV submission')
print()
# %%

# AVERAGE SECOND WEEK FORECAST (Please choose this for the 2nd week CSV entry).
flow_mean2 = ((data['flow'].tail(14)).mean())  # .round(2)
print('The AVERAGE forecast for the SECOND week that comes is:', flow_mean2,
      'cf/s.')
print('Use this value for the 2nd week CSV submission')
print()

# %%
# Another example but this time using two time lags as inputs to the model
model2 = LinearRegression()
x2 = train[['flow_tm1', 'flow_tm2']]
model2.fit(x2, y)
r_sq = model2.score(x2, y)
print('coefficient of determination:', np.round(r_sq, 2))
print()
print('intercept:', np.round(model2.intercept_, 2))
print()
print('slope:', np.round(model2.coef_, 2))
print()

# generate predictions with the function
q_pred2_train = model2.predict(train[['flow_tm1', 'flow_tm2']])

# or by hand
q_pred2 = model2.intercept_   \
         + model2.coef_[0] * train['flow_tm1'] \
         + model2.coef_[1] * train['flow_tm2']

# %%
# Here are some examples of things you might want to plot to get you started:

# 1. Timeseries of observed flow values
# Note that date is the index for the dataframe so it will
# automatically treat this as our x axis unless we tell it otherwise
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], label='full', color='black', linewidth=0.5)
ax.plot(train['flow'], 'r:', label='training', color='aqua', linestyle='-',
        alpha=0.5, linewidth=4)
ax.set(title="1. Entire Flow Data Since 1989", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]",
       yscale='log')
ax.legend()

# An example of saving your figure to a file
fig.set_size_inches(7, 5)
fig.savefig("1. Entire Flow Data Since 1989.png")

# 2. Time series of flow values with the x axis range limited
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], label='full', color='black', linewidth=0.5)
ax.plot(train['flow'], 'r:', label='training', color='aqua', linestyle='-',
        alpha=0.5, dash_capstyle='round', linewidth=4)
ax.plot(test['flow'], 'r:', label='testing', color='gold', linestyle='-',
        alpha=0.5, dash_capstyle='round', linewidth=4)
ax.set(title="2. Testing, Training & Real Flow", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]",
       yscale='log', xlim=[datetime.date(1996, 8, 24),
                           datetime.date(2021, 1, 1)])
ax.legend()
fig.set_size_inches(7, 5)
fig.savefig("2. Testing, Training & Real Flow.png")

# 3. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['flow'], color='purple', linewidth=2, label='observed')
ax.plot(train.index, q_pred_train, color='aqua', linestyle='-',
        label='simulated')
ax.set(title="3. Flow Simulation Done", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]",
       yscale='log')
ax.legend()

# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("3. Flow Simulation Done.png")

# 4. Scatter plot of t vs t-1 flow with log log axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='*',
           color='purple', label='obs')
ax.set(title="4. Autoregression Model", xlabel='flow t-1', ylabel='flow t',
       yscale='log', xscale='log')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model',
        color='aqua', linewidth=3)
ax.legend()

# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("4. Autoregression Model.png")

# 5. Scatter plot of t vs t-1 flow with normal axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='*',
           color='purple', label='observations')
ax.set(title="5. Autoregression Model", xlabel='flow t-1', ylabel='flow t',
       xlim=[0, 500], ylim=[0, 500])
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model',
        color='aqua', linewidth=3)
ax.legend()

# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("5. Autoregression Model.png")

# Xenia: Showing all my plots as an output
plt.show()

# %%
