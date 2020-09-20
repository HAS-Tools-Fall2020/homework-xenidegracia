# Start code for assignment 3
# this code sets up the lists you will need for your homework
# and provides some examples of operations that will be helpful to you

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
datapath = 'C:/Users/xy_22/Documents/MSc._Hydrology/2020_Fall/599-HAS_Tools/homework-xenidegracia/data'
filename = 'streamflow_week3.txt'
filepath = os.path.join(datapath,filename)
print(os.getcwd())
print(filepath)
os.path.exists(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

# Read the data into a pandas dataframe
# Xenia changed the number of rows to skip
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# make lists of the data
flow = data.flow.values.tolist()
date = data.datetime.values.tolist()
year = data.year.values.tolist()
month = data.month.values.tolist()
day = data.day.values.tolist()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Here is some starter code to illustrate some things you might like to do
# Modify this however you would like to do your homework. 
# From here on out you should use only the lists created in the last block:
# flow, date, year, month and day

# Calculating some basic properites
print("Type of the Flow variable is =",type(flow))
print("Type of the Date variable is =",type(date))
print("Type of the Year variable is =",type(year))
print("Type of the Month variable is =",type(month))
print("Type of the Day variable is =",type(day))
print('Lenght of the variables flow,  date, year, month and day =',len(flow))
print('The minimum flow of all the data since 1989 was =',min(flow))
print('The maximum flow of all the data  since 1989 was =',max(flow))
print('The mean flow of all the data  since 1989 was =',np.mean(flow))
print('The standar deviation of all the data  since 1989 was =',np.std(flow))

# %%
ReferenceData = len(date) - 21

# Making and empty list that I will use to store
# index values I'm interested in
FirstWeekSeptDate = []
FirstWeekSeptFlowTotal = []
FirstWeekSeptFlowBefore2000 = []
FirstWeekSeptFlowAfter2010 = []
SecondWeekSeptDate = []
SecondWeekSeptFlowTotal = []
SecondWeekSeptFlowBefore2000 = []
SecondWeekSeptFlowAfter2010 = []
FirstHalfSeptember = []
SecondHalfSeptember = []


# Loop over the length of the flow list
# and adding the index value to the ilist
# if it meets some criteria that I specify

# For my September's First Week prediction, the flow was 171.816
for i in range(len(flow)):
    if flow [i] > 171.816 and month[i] == 9:
        FirstWeekSeptFlowTotal.append(i)
    if flow [i] > 171.816 and month[i] == 9 and year[i]<=2000:
        FirstWeekSeptFlowBefore2000.append(i)
    if flow [i] > 171.816 and month[i] == 9 and year[i]>=2010:
        FirstWeekSeptFlowAfter2010.append(i)
print('The minimum flow of 1st Week Sept 2020 was =',min(FirstWeekSeptFlowTotal))
print('The maximum flow  of  1st Week Sept 2020 was =',max(FirstWeekSeptFlowTotal))
print('The mean flow of 1st Week Sept 2020 was =',np.mean(FirstWeekSeptFlowTotal))
print('The standar deviation of 1st Week Sept 2020 was =',np.std(FirstWeekSeptFlowTotal))                
                
 # %%               
# For my September's Second Week prediction, the flow was 53.6                
for i in range(len(flow)):
    if flow [i] > 53.6 and month[i] == 9:
        SecondWeekSeptFlowTotal.append(i)
    if flow [i] > 53.6 and month[i] == 9 and year[i]<=2000:
         SecondWeekSeptFlowBefore2000.append(i)
    if flow [i] > 53.6 and month[i] == 9 and year[i]>=2010:
        SecondWeekSeptFlowAfter2010.append(i)
print('The minimum flow of 2nd Week Sept 2020 was =',min(SecondWeekSeptFlowTotal))
print('The maximum flow  of  2nd Week Sept 2020 was =',max(SecondWeekSeptFlowTotal))
print('The mean flow of 2nd Week Sept 2020 was =',np.mean(SecondWeekSeptFlowTotal))
print('The standar deviation of 2nd Week Sept 2020 was =',np.std(SecondWeekSeptFlowTotal))  
                
# %%              
# Grabbing out the data from the first and second half of September of all the years              
for i in range(len(flow)):
    if  month[i] ==9 and day[i] <= 15:
        FirstHalfSeptember.append(i)

    if month[i] ==9 and day[i] >= 16 and day[i] <= 30:
        SecondHalfSeptember.append(i)                
         

FirstWeekTotalGreaterPercentage = (len(FirstWeekSeptFlowTotal) / len(flow))*100
FirstWeekBefore2000GreaterPercentage = (len(FirstWeekSeptFlowBefore2000) / len(flow))*100
FirstWeekAfter2010GreaterPercentage = (len(FirstWeekSeptFlowAfter2010) / len(flow))*100
SecondWeekTotalGreaterPercentage = (len(SecondWeekSeptFlowTotal) / len(flow))*100
SecondWeekBefore2000GreaterPercentage = (len(SecondWeekSeptFlowBefore2000) / len(flow))*100
SecondWeekAfter2010GreaterPercentage = (len(SecondWeekSeptFlowAfter2010) / len(flow))*100

                
# see how many times the criteria was met by checking the length
# of the index list that was generated
print("Times that the flow was greater than my 1st week prediction =",len(FirstWeekSeptFlowTotal))
print("Times that the flow was greater than my 1st week prediction Before year 2000 =",len(FirstWeekSeptFlowBefore2000))
print("Times that the flow was greater than my 1st week prediction After year 2010 =",len(FirstWeekSeptFlowAfter2010))
print("Times in % that the daily flow was greater than my 1st week prediction =",FirstWeekTotalGreaterPercentage, "%")
print("Times in % that the daily flow was greater than my 1st week prediction Before year 2000 =",FirstWeekBefore2000GreaterPercentage, "%")
print("Times in % that the daily flow was greater than my 1st week prediction After year 2010 =",FirstWeekAfter2010GreaterPercentage, "%")


print("Times that the flow was greater than my 2nd week prediction =",len(SecondWeekSeptFlowTotal))
print("Times that the flow was greater than my 2nd week prediction Before year 2000 =",len(SecondWeekSeptFlowBefore2000))
print("Times that the flow was greater than my 2nd week prediction After year 2010 =",len(SecondWeekSeptFlowAfter2010))
print("Times in % that the daily flow was greater than my 2nd week prediction =",SecondWeekTotalGreaterPercentage, "%")
print("Times in % that the daily flow was greater than my 2nd week prediction Before year 2000 =",SecondWeekBefore2000GreaterPercentage, "%")
print("Times in % that the daily flow was greater than my 2nd week prediction After year 2010 =",SecondWeekAfter2010GreaterPercentage, "%")

# %%
# Grabbing out the data that met the criteria
# This  subset of data is just the elements identified 
# in the ilist
FirstHalfSeptemberFlow = [flow[j] for j in FirstHalfSeptember]
SecondHalfSeptemberFlow = [flow[j] for j in SecondHalfSeptember]
MeanFlowFirstHalfSeptember = np.mean(FirstHalfSeptemberFlow)
MeanFlowSecondHalfSeptember = np.mean(SecondHalfSeptemberFlow)
if MeanFlowFirstHalfSeptember > MeanFlowSecondHalfSeptember:
    print("The mean flow of the First Half of September is greater than the mean flow of the Second Half")
if MeanFlowFirstHalfSeptember < MeanFlowSecondHalfSeptember:
    print("The mean flow of the First Half of September is less than the mean flow of the Second Half")

# %%
