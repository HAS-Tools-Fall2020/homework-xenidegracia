# Starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
datapath = 'C:/Users/xy_22/Documents/MSc._Hydrology/2020_Fall/599-HAS_Tools/homework-xenidegracia/data'
filepath = os.path.join(datapath, filename)
print(os.getcwd())

print(filepath)
# XDG. This shows if the path exists or not
os.path.exists(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()
# XDG. Print the type, dimension and shape of "flow_data" variable
print('The type of flow_data is:',type(flow_data))
print('The values stored within "flow_data" are all type:',type(flow_data[0,0]))
print('The dimension of flow_data is:',flow_data.ndim)
print('The shape of the flow_data is:', flow_data.shape)

# XDG. I needed to see how my numpy looked like.
print(flow_data)
# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Summary of the entire Data
print('The minimum flow of all the data since 1989 was =',min(flow_data[:,3]))
print('The maximum flow of all the data  since 1989 was =',max(flow_data[:,3]))
print('The mean flow of all the data  since 1989 was =',np.mean(flow_data[:,3]))
print('The standard deviation of all the data  since 1989 was =',np.std(flow_data[:,3]))

# %%
# Starter Code

# FIRST WEEK FORECAST
# Count the number of values with days < 19 and month ==9 and year ==2020
StudyYear = 2020
StudyMonth = 9
StudyDays = 19
flow_count = np.sum((flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays))

# this gives a list of T/F where the criteria are met
(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays)


# this give the flow values where that criteria is met
flow_pick = flow_data[(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays), 3]


# this give the year values where that criteria is met
year_pic = flow_data[(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays), 0]


# this give the all rows where that criteria is met
all_pic = flow_data[(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays), ]


# Calculate the average flow for these same criteria 
flow_mean = np.mean(flow_data[(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays),3])

print("Flow meets this critera (days<19 & month=9 & year=2020):", flow_count, " times.")
print('And has an average value of:', flow_mean, "when this is true.")
print('So the forecast for the FIRST week that comes is:', flow_mean,'cf/s.')


# %%
# SECOND WEEK FORECAST
StudyYear = 2020
StudyMonth = 9
StudyDays = 14

# Count the number of values with days < 14 and month ==9 and year ==2020
flow_count2 = np.sum((flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays))

# this gives a list of T/F where the criteria are met
(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays)


# this give the flow values where that criteria is met
flow_pick2 = flow_data[(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays), 3]


# this give the year values where that criteria is met
year_pic2 = flow_data[(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays), 0]


# this give the all rows where that criteria is met
all_pic2 = flow_data[(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays), ]


# Calculate the average flow for these same criteria 
flow_mean2 = np.mean(flow_data[(flow_data[:,0] == StudyYear) & (flow_data[:,1]==StudyMonth) & (flow_data[:,2] <= StudyDays),3])

print("Flow meets this critera (days<14 and month==9 and year==2020):", flow_count2, " times.")
print('And has an average value of:', flow_mean2, "when this is true.")
print('So the forecast for the SECOND week that comes is:', flow_mean2,'cf/s.')


# %%
#For my September's First Week prediction, the flow was 171.816
FirstWeekFlowPrediction = 171.816

# Count the number of values greater than my First Week Prediction. And also before 2000, and after 2010.
flow_count3 = np.sum((flow_data[(flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), 3]))
flow_count4 = np.sum((flow_data[(flow_data[:,0]<=2000) & (flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), 3]))
flow_count5 = np.sum((flow_data[(flow_data[:,0]>=2010) & (flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), 3]))

flow_countTotalDaysMonth = np.sum(flow_data[:,1]==StudyMonth)
flow_countFlowOver = np.sum((flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction))
percentage = [flow_countFlowOver/flow_countTotalDaysMonth]*100


# this give the flow values where that criteria is met
flow_pick3 = flow_data[(flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), 3]

flow_pick4 = flow_data[(flow_data[:,0]<=2000) & (flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), 3]

flow_pick5 = flow_data[(flow_data[:,0]>=2010) & (flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), 3]


# this give the year values where that criteria is met
year_pic3 = flow_data[(flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), 0]

year_pic4 = flow_data[(flow_data[:,0]<=2000) & (flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), 0]

year_pic5 = flow_data[(flow_data[:,0]>=2010) & (flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), 0]


# this give the all rows where that criteria is met
all_pic3 = flow_data[(flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), ]

all_pic4 = flow_data[(flow_data[:,0]<=2000) & (flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), ]

all_pic5 = flow_data[(flow_data[:,0]>=2010) & (flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction), ]


# Calculate the average flow for these same criteria 
flow_mean3 = np.mean(flow_data[(flow_data[:,1]==StudyMonth) & (flow_data[:,3] >= FirstWeekFlowPrediction),3])

print("Flow was greater than my First prediction:", flow_count3, " times.")
print("In percentage, the flow was greater than my First prediction:",percentage, " %.")
print('And has an average value of', flow_mean3, "when this is true.")
print("Before 2000, Flow was greater than my First prediction:", flow_count4, " times.")
print("After 2010, Flow was greater than my First prediction:", flow_count5, " times.")



# %%
# Make a histogram of data
# Use the linspace  function to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cf/s]')
plt.ylabel('Count')

# Get the quantiles of flow
# Two different approaches ---  you should get the same answer
# just using the flow column
flow_quants1 = np.quantile(flow_data[:,3], q=[0,0.1, 0.5, 0.9])
print('Method one flow quantiles:', flow_quants1)
# Or computing on a colum by column basis 
flow_quants2 = np.quantile(flow_data, q=[0,0.1, 0.5, 0.9], axis=0)
# and then just printing out the values for the flow column
print('Method two flow quantiles:', flow_quants2[:,3])

# %%
