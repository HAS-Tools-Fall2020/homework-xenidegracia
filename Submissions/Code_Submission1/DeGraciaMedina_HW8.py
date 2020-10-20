# Week 8: Final graded script from section 1

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from yellowbrick.datasets import load_concrete
from yellowbrick.regressor import ResidualsPlot

# Note: you may need to do pip install for sklearn

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data

# ACTION REQUIRED: change the name of the file with the current number of \
# the week
filename = 'streamflow_week8.txt'

# LC - nice print statements 
# The variable "filepath" will automatically join the address of your data \
# and the document.
filepath = os.path.join('../../data', filename)
print('The current work directory is:')
print(os.getcwd())
print()
print('The data is storaged at:')
print(filepath)
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
                     parse_dates=['datetime'],
                     )

# Expand the dates to year, month, day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
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

# %%
# Step 2 - pick what portion of the time series you want to use as training \
# data

# Xenia: Converting the training years to weeks.
# FUNCTION to convert the specific training years, to weeks.


def StudyYears_to_weeks(number_of_year):
    """ It converts the quantity of years, to weeks and rounded to two
    decimals.

    Parameters
    ----------
    number_of_year : int
                    Start or final year for training

    Returns
    ------
    conversion1 : str, int
                  It converst the year to weeks
    """

    conversion1 = round(((number_of_year - 1989)*52), 2)

    return conversion1


start_train_week = StudyYears_to_weeks(1996)
final_train_week = StudyYears_to_weeks(2004)

# Idecided to not use this method of taking data. So I used the netx location \
# by datetime.

# %%
# Xenia: Taking train data from August to December 2019 because it was a dry \
# year too.

train = flow_weekly.loc["2019-08-22":"2019-12-12"][[
      'flow', 'flow_tm1', 'flow_tm2']]
# This shows the start and end of the training data.
print("The training data was taken from ", train.index.min(), " to ",
      train.index.max())
print()

# Xenia: Taking test data from last 3 years. Convert years to weeks through
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

# %%
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

# %%
# Step 4 Make a prediction with your model
# Predict the model response for a given flow value
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1, 1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1, 1))

# Alternatively you can calcualte this yourself like this:
# Xenia: y = b + m(x)
q_pred = (model.intercept_ + (model.coef_ * train['flow_tm1'])).round(2)

# Xenia: Printing the final equation of the model
print('The AR model equation is:  y =', model.intercept_.round(2), '+',
      model.coef_.round(2), 'X')
print()

# Xenia: Printing the seasonal prediction.
# Xenia: Please use this value for the Regression based Forecast.
print('Seasonal predictions using Linear Regression are:',
      q_pred)
print()

# %%
# AR model for WEEKLY forecast

# Xenia: I used the minimum value of the last 3 WEEKS to forecast the \
# coming week.
# Xenia: Please USE this value for AR prediction.


def weeklyforecast(i):
    """
      AR model for weekly predictions.

      INPUT
      i : float
          Value of the quantity of weeks we want to take into account for the
          AR model.

      OUTPUT
      past_weeks : float
      weekly_AR_pred : float
      """

    past_weeks = flow_weekly['flow'][-i]
    weekly_AR_pred = (model.intercept_ + model.coef_ * past_weeks).round(2)
    return weekly_AR_pred


for i in range(2, 4):
    print('The AR values for the next', i-1, 'week is:', weeklyforecast(i))


print()

# %%
# My initial forecast method was using just average of the last weeks:

# AVERAGE FIRST WEEK FORECAST.
flow_mean1 = round(((data['flow'].tail(21)).mean()), 2)  # .round(2)
print('The AVERAGE forecast for the FIRST week that comes is:', flow_mean1,
      'cf/s.')
print()
# %%
# AVERAGE SECOND WEEK FORECAST.
# LC - i'm a little confused about the tail 14 here? 
flow_mean2 = ((data['flow'].tail(14)).mean()).round(2)  # .round(2)
print('The AVERAGE forecast for the SECOND week that comes is:', flow_mean2,
      'cf/s.')
print()

# %%
# SEASONAL FORECAST based just on average of 2019
# Locating my data from August to December 2019
data2019 = flow_weekly.loc["2019-08-22":"2019-12-12"]

# Printing my 16 values for seasonal forecast
# LC - you could also save this to a variable 
for i in range(16):
    print('Week #', i+1, 'forecast:', data2019['flow'][i])

# %%
# Another example but this time using two time lags as inputs to the model
# LC - A little confused about how this part fits in with the rest. 
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
# PLOTS

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

# Saving the figure to a file
fig.set_size_inches(7, 5)
fig.savefig("1._Entire_Flow_Data_Since_1989.png")

# 2. Time series of flow values with the x axis range limited
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], label='full', color='black', linewidth=0.5)
ax.plot(test['flow'], 'r:', label='testing', color='gold', linestyle='-',
        alpha=0.5, dash_capstyle='round', linewidth=4)
ax.plot(train['flow'], 'r:', label='training', color='aqua', linestyle='-',
        dash_capstyle='round', linewidth=4)
ax.set(title="2. Testing, Training & Real Flow", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]",
       yscale='log', xlim=[datetime.date(2014, 8, 24),
                           datetime.date(2021, 1, 15)])
ax.legend()
fig.set_size_inches(7, 5)
fig.savefig("2._Testing,_Training_&_Real_Flow.png")

# 3. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['flow'], color='purple', linewidth=2, label='observed')
ax.plot(train.index, q_pred_train, color='aqua', linestyle='-',
        label='simulated')
ax.set(title="3. Flow Simulation Done", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]",
       yscale='log')
plt.xticks(rotation=30)

# This above was to rotate the datetime axis to avoid the \
# overlapping.
ax.legend()

# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("3._Flow_Simulation_Done.png")
# %%
# 4. Scatter plot of t vs t-1 flow with log log axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='.',
           color='purple', label='obs')
ax.set(title="4. Autoregression Model", xlabel='flow t-1', ylabel='flow t',
       yscale='log', xscale='log', xlim=[0, 200], ylim=[0, 200])
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model',
        color='aqua', linewidth=3)
ax.legend()

# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("4._Autoregression_Model.png")

# 5. Scatter plot of t vs t-1 flow with normal axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='.',
           color='purple', label='observations')
ax.set(title="5. Autoregression Model", xlabel='flow t-1', ylabel='flow t',
       xlim=[0, 175], ylim=[0, 175])
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model',
        color='aqua', linewidth=3)
ax.legend()

# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("5._Autoregression_Model.png")

# Xenia: Showing all my plots as an output
plt.show()

# %%
# Residuals Plot (Trying new things)

# The residuals plot shows how the model is injecting error, the bold \
# horizontal line at residuals = 0 is no error, and any point above or below \
# that line, indicates the magnitude of error.
# (https://www.scikit-yb.org/en/latest/quickstart.html#installation)

# Load a regression dataset
X, y = load_concrete()

# %%
# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

visualizer = ResidualsPlot(LinearRegression())
visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()                 # Finalize and render the figure

# Xenia: Saving my plots
plt.show()
fig.set_size_inches(7, 5)
plt.savefig("6._Residuals_Plot.png")
fig.savefig("6._Residuals_Plot.png")

# %%
