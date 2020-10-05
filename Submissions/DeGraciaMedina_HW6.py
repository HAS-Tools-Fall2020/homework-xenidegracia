# Starter code for week 6 illustrating how to build an AR model 
# and plot it

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
#note you may need to do pip install for sklearn

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week6.txt'
# Xenia: Create a datapath variable to ensure the correct address
datapath = 'C:/Users/xy_22/Documents/MSc._Hydrology/2020_Fall/599-HAS_Tools/homework-xenidegracia/data'
filepath = os.path.join(datapath, filename)
print(os.getcwd())
print(filepath)
# Xenia: This shows if the path exists or not
os.path.exists(filepath)


# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek
# Xenia: Note that Now Mondays are represented by dayofweek=0 and Sundays are represented by dayofweek=6

# Aggregate flow values to weekly
flow_weekly = data.resample("W", on='datetime').mean().round(2)
# Xenia: Added the round function to 2 decimals.

# %%
# Building an autoregressive model 
# You can learn more about the approach I'm following by walking 
# Through this tutorial
# https://realpython.com/linear-regression-in-python/

# Step 1: setup the arrays you will build your model on
# This is an autoregressive model so we will be building
# it based on the lagged timeseries

flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)

# Step 2 - pick what portion of the time series you want to use as training data
# here I'm grabbing the first 800 weeks 
# Note1 - dropping the first two weeks since they wont have lagged data
# to go with them  
# Xenia: Taking data from 1996 to 2004 (2008,2017) because you only live once?
train = flow_weekly[364:780][['flow', 'flow_tm1', 'flow_tm2']]
# Xenia: Taking data from last 3 years to test
test = flow_weekly[-156:][['flow', 'flow_tm1', 'flow_tm2']]

# Step 3: Fit a linear regression model using sklearn 
x=train['flow_tm1'].values.reshape(-1,1) #See the tutorial to understand the reshape step here 
y=train['flow'].values
# Xenia: Shorten the steps to create the regression model
model = LinearRegression().fit(x,y)

#Look at the results
# r^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq,2))

#print the intercept and the slope 
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# Step 4 Make a prediction with your model 
# Predict the model response for a  given flow value
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1,1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1,1))

#alternatively you can calcualte this yourself like this: 
# Xenia: y = b + m(x)
q_pred = model.intercept_ + (model.coef_ * train['flow_tm1'])
# Xenia: Printing the equation of the model
print('The AR model equation is:  y =' , model.intercept_.round(2) , '+' , model.coef_.round(2),'X')
# Xenia: Printing my prediction value. (I used thi minimun value of the range.)
print('Prediction using equation from Linear Regression is:',q_pred.min().round(2))

# %%
# you could also predict the q for just a single value like this
# Xenia: I used the minimum value of the last 3 WEEKS to forecast the coming week.
# Xenia: I made the same to predict the second week value, but using the minimun flow of the data from the LAST week only.
last_week_flow = flow_weekly['flow'][-3].min()
last2_weeks_flow = flow_weekly['flow'][-1].min()
prediction1stweek = model.intercept_ + model.coef_ * last_week_flow
prediction2ndweek = model.intercept_ + model.coef_ * last2_weeks_flow
# Xenia: Printing the equation of the model
print('First week prediction based on my 3 last week average value is:',prediction1stweek.round(2))
print('Second week prediction based on my last weeks average value is:',prediction2ndweek.round(2))


# %%
# To compare with my initial method using just average of the last weeks:

# AVERAGE FIRST WEEK FORECAST
flow_mean1=((data['flow'].tail(21)).mean()).round(2)
print('The AVERAGE forecast for the FIRST week that comes is:',flow_mean1,'cf/s.')
print()

# AVERAGE  SECOND WEEK FORECAST
flow_mean2=((data['flow'].tail(14)).mean()).round(2)
print('The AVERAGE forecast for the SECOND week that comes is:',flow_mean2,'cf/s.')
print()

# %%
# Another example but this time using two time lags as inputs to the model 
model2 = LinearRegression()
x2=train[['flow_tm1','flow_tm2']]
model2.fit(x2,y)
r_sq = model2.score(x2, y)
print('coefficient of determination:', np.round(r_sq,2))
print('intercept:', np.round(model2.intercept_, 2))
print('slope:', np.round(model2.coef_, 2))

# generate predictions with the function
q_pred2_train = model2.predict(train[['flow_tm1', 'flow_tm2']])

# or by hand
q_pred2 = model2.intercept_   \
         + model2.coef_[0]* train['flow_tm1'] \
         +  model2.coef_[1]* train['flow_tm2'] 

# %% 
# Here are some examples of things you might want to plot to get you started:

# 1. Timeseries of observed flow values
# Note that date is the index for the dataframe so it will 
# automatically treat this as our x axis unless we tell it otherwise
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], label='full', color='grey')
ax.plot(train['flow'], 'r:', label='training', color='aqua', linestyle='-', alpha=0.50)
ax.set(title="1. Entire Flow Data Since 1989", xlabel="Date", 
        ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend()
# an example of saving your figure to a file
fig.set_size_inches(7,5)
fig.savefig("1. Entire Flow Data Since 1989.png")

#2. Time series of flow values with the x axis range limited
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], label='full', color='grey')
ax.plot(train['flow'], 'r:', label='training', color='aqua', linestyle='-', alpha=0.50, dash_capstyle='round')
ax.plot(test['flow'], 'r:', label='testing', color='gold', linestyle='-', alpha=0.50, dash_capstyle='round')
ax.set(title="2. Testing, Training & Real Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log', xlim=[datetime.date(1996, 8, 24), datetime.date(2021, 1, 1)])
ax.legend()
fig.set_size_inches(7,5)
fig.savefig("2. Testing, Training & Real Flow.png")

# 3. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['flow'], color='purple', linewidth=2, label='observed')
ax.plot(train.index, q_pred_train, color='aqua', linestyle='-', 
        label='simulated')
ax.set(title="3. Flow Simulation Done", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend()
# Xenia: Saving my plots
fig.set_size_inches(7,5)
fig.savefig("3. Flow Simulation Done.png")

# 4. Scatter plot of t vs t-1 flow with log log axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='*',
              color='purple', label='obs')
ax.set(title="4. Autoregression Model", xlabel='flow t-1', ylabel='flow t', yscale='log', xscale='log')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model', color='aqua')
ax.legend()
# Xenia: Saving my plots
fig.set_size_inches(7,5)
fig.savefig("4. Autoregression Model.png")

# 5. Scatter plot of t vs t-1 flow with normal axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='*',
              color='purple', label='observations')
ax.set(title="5. Autoregression Model", xlabel='flow t-1', ylabel='flow t')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model', color='aqua')
ax.legend()
# Xenia: Saving my plots
fig.set_size_inches(7,5)
fig.savefig("5. Autoregression Model.png")

plt.show()

# %%
# Playing with plots

