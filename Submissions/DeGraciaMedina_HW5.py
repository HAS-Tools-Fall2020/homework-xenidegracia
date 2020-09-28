# Starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import earthpy as et
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
datapath = 'C:/Users/xy_22/Documents/MSc._Hydrology/2020_Fall/599-HAS_Tools/homework-xenidegracia/data'
filepath = os.path.join(datapath, filename)
print(os.getcwd())
print(filepath)
# XDG. This shows if the path exists or not
os.path.exists(filepath)

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )
print(data.head(0))
print()

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)
# Printing my new "data"
print(data)
print()

# %%
# Answer Question #1. Print the type, dimension and shape of "flow_data" variable
print('The type of "data" is:',type(data))
print()
print('The values stored within "data" are all type:',data.info())
print()
print('The dimension of the dataframe "data" is:',data.ndim)
print()
print('The total size of the dataframe "data" is:',data.size,'. It means \
that it has:',data.size, 'elements.')
print()
print('The shape of the dataframe "data" is:', data.shape)
print()

# %%
# Answer Question #2. Summary of the entire Data
print('The min.,max.,mean,std and quantiles of the flow since 1989 is:')
print(np.round(data[["flow"]].describe(),decimals=2))

# %%
# Answer Question #3. Quantiles per month
MonthlyFlow= data.groupby(['month'])[['flow']].describe()
print(np.round(MonthlyFlow,decimals=2))

# %%
# Answer Question #4. Showing the 5 max values and the 5 min values
data.sort_values(by=('flow'), ascending = False)

# %%
# Answer Question #5. Highest and lowest flow values for every month.
JanuaryFlows = data[data["month"] == 1]
print('January flow values are:')
print(JanuaryFlows.sort_values(by=('flow'), ascending = False))
print()
print()

FebruaryFlows = data[data["month"] == 2]
print('February flow values are:')
print(FebruaryFlows.sort_values(by=('flow'), ascending = False))
print()
print()

MarchFlows = data[data["month"] == 3]
print('March flow values are:')
print(MarchFlows.sort_values(by=('flow'), ascending = False))
print()
print()

AprilFlows = data[data["month"] == 3]
print('April flow values are:')
print(AprilFlows.sort_values(by=('flow'), ascending = False))
print()
print()

MayFlows = data[data["month"] == 3]
print('May flow values are:')
print(MayFlows.sort_values(by=('flow'), ascending = False))
print()
print()

JuneFlows = data[data["month"] == 3]
print('June flow values are:')
print(JuneFlows.sort_values(by=('flow'), ascending = False))
print()
print()

JulyFlows = data[data["month"] == 3]
print('July flow values are:')
print(JulyFlows.sort_values(by=('flow'), ascending = False))
print()
print()

AugustFlows = data[data["month"] == 3]
print('August flow values are:')
print(AugustFlows.sort_values(by=('flow'), ascending = False))
print()
print()

SeptemberFlows = data[data["month"] == 3]
print('September flow values are:')
print(SeptemberFlows.sort_values(by=('flow'), ascending = False))
print()
print()

OctoberFlows = data[data["month"] == 3]
print('October flow values are:')
print(OctoberFlows.sort_values(by=('flow'), ascending = False))
print()
print()

NovemberFlows = data[data["month"] == 3]
print('November flow values are:')
print(NovemberFlows.sort_values(by=('flow'), ascending = False))
print()
print()

DecemberFlows = data[data["month"] == 3]
print('December flow values are:')
print(DecemberFlows.sort_values(by=('flow'), ascending = False))
print()

# %%
# Answer Question #6. Dates with flows that are within 15% of my week 1 forecast value.
#For my September's First Week prediction, the flow was 171.816 cf/s

FirstWeekFlowPrediction = 171.816
PercentageWindow = 0.15*FirstWeekFlowPrediction

FlowsWithinPercentageWindow = data[data["flow"] <= PercentageWindow]
print(np.round(FlowsWithinPercentageWindow,decimals=2))

# %%
# Plot the data in line plot
f, ax = plt.subplots(1,1)
ax.plot(MonthlyFlow[('flow', 'mean')],color="turquoise")
ax.set(title="Mean Monthly Flows in cf/s since 1989")

# %%
# Plot the data in bar plot
f, ax = plt.subplots()
ax.bar(MonthlyFlow.index,
        MonthlyFlow[('flow', 'mean')],
        color="fuchsia")
ax.set(title="Mean Monthly Flows in cf/s since 1989")
plt.show()

# %%
# FIRST WEEK FORECAST
flow_mean1=((data['flow'].tail(21)).mean()).round(2)
print('The forecast for the FIRST week that comes is:',flow_mean1,'cf/s.')
print()

# %%
# SECOND WEEK FORECAST
flow_mean2=((data['flow'].tail(14)).mean()).round(2)
print('The forecast for the SECOND week that comes is:',flow_mean2,'cf/s.')
print()

# %%
# Seasonal Forecast
StudyYear = 2019

StudyMonth = 8
Week = 1
StartDay = 22
LastDay = 29
Seasonal_meanW1 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW1).describe())
print()

StudyMonth = 9
Week = Week + 1
StartDay = 1
LastDay = 5
Seasonal_meanW2 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW2).describe())
print()

StudyMonth = 9
Week = Week + 1
StartDay = 6
LastDay = 12
Seasonal_meanW3 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW3).describe())
print()

StudyMonth = 9
Week = Week + 1
StartDay = 13
LastDay = 19
Seasonal_meanW4 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW4).describe())
print()

StudyMonth = 9
Week = Week + 1
StartDay = 20
LastDay = 26
Seasonal_meanW5 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW5).describe())
print()

StudyMonth = 9
Week = Week + 1
StartDay = 27
LastDay = 31
Seasonal_meanW6 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW6).describe())
print()

StudyMonth = 10
Week = Week + 1
StartDay = 4
LastDay = 10
Seasonal_meanW7 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW7).describe())
print()

StudyMonth = 10
Week = Week + 1
StartDay = 11
LastDay = 17
Seasonal_meanW8 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW8).describe())
print()

StudyMonth = 10
Week = Week + 1
StartDay = 18
LastDay = 24
Seasonal_meanW9 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW9).describe())
print()

StudyMonth = 10
Week = Week + 1
StartDay = 25
LastDay = 31
Seasonal_meanW10 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW10).describe())
print()

StudyMonth = 11
Week = Week + 1
StartDay = 1
LastDay = 7
Seasonal_meanW11 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW11).describe())
print()

StudyMonth = 11
Week = Week + 1
StartDay = 8
LastDay = 14
Seasonal_meanW12 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW12).describe())
print()

StudyMonth = 11
Week = Week + 1
StartDay = 15
LastDay = 21
Seasonal_meanW13 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW13).describe())
print()

StudyMonth = 11
Week = Week + 1
StartDay = 22
LastDay = 28
Seasonal_meanW14 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW14).describe())
print()

StudyMonth = 12
Week = Week + 1
StartDay = 1
LastDay = 5
Seasonal_meanW15 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW15).describe())
print()

StudyMonth = 12
Week = Week + 1
StartDay = 6
LastDay = 12
Seasonal_meanW16 = (data[(data['year']==StudyYear) & (data['month']==StudyMonth) & (data["day"]>=StartDay) & (data["day"]<=LastDay)][["flow"]])
print('The Seasonal forecast for week',Week,'(from',StartDay,'to',LastDay,'of the month',StudyMonth,') is:')
print((Seasonal_meanW16).describe())
print()

# %%
# Make a histogram of data

# Use the linspace  function to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=25)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 
#Plotting the histogram
plt.hist(data[['flow']], bins = mybins, color=('lightblue'))
plt.title('Streamflow')
plt.xlabel('Flow [cf/s]')
plt.ylabel('Count')
plt.show()

mybins3 = np.linspace(0, 300, num=25)
#Plotting the histogram
plt.hist(data[['flow']],bins = mybins3)
plt.title('Streamflow')
plt.xlabel('Flow [cf/s]')
plt.ylabel('Count')
plt.show()

# %%
