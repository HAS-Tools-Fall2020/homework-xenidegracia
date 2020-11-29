
# Paper title: A global dataset of surface water and groundwater salinity measurements from 1980-2019
# Data citation: Thorslund, Josefin; van Vliet, Michelle T H (2020): A global salinity dataset of surface water and groundwater measurements from 1980-2019. PANGAEA, https://doi.pangaea.de/10.1594/PANGAEA.913939 

# Data set creator:  Josefin Thorslund - Stockholm University & Utrecht University
# Data set creator:  Michelle van Vliet - Utrecht University

############################################################################################################################

# Clear console and list
rm(list=ls())
cat("\014") 

# Set working directory and load packages
setwd("") #choose your file location

#Load packages and functions 
require(data.table)
require(dplyr)


############################################################################################################################
## Function that computes the descriptive stats for the summary files

fileNames <- c("Groundwaters_database.csv", "Rivers_database.csv", "Lakes_Reservoirs_database.csv") ## All database files

extension <- "csv"

fileNumbers <- seq(fileNames)

for (fileNumber in fileNumbers) {
  
  newFileName <-  paste("summary_",
                        fileNames[fileNumber])
  
  #Read files as data.tables and fix formats
  data.file=fread(fileNames[fileNumber]) 
  data.file$Date=as.Date(data.file$Date, format="%Y-%m-%d")
  data.file$EC=as.numeric(data.file$EC)
  
  setDT(data.file)[order(Date), head(.SD, 1L), by = Station_ID]
  
  #find first and last sample date for each sampling location (Station_ID)
  Start_date=data.file %>% 
    group_by(Station_ID) %>%
    filter(Date == min(Date))
  
  
  end_date=data.file %>% 
    group_by(Station_ID) %>%
    filter(Date == max(Date))
  
  
  Start_date=Start_date[,c(1,6)]
  end_date=end_date[,c(1,6)]
  
  
  names(Start_date)[names(Start_date) == "Date"] <- "Start_date"
  names(end_date)[names(end_date) == "Date"] <- "End_date"
  Dates_info=left_join(Start_date,end_date, by="Station_ID")
  
  #compute stats for each station ID
  stats=data.file[,list( n=length(EC), median=median(EC), mean=mean(EC), max=max(EC), min=min(EC), sd=sd(EC))
                  ,by=list(Station_ID=Station_ID)]
  
  
  # join the stats and the sampling date (start, end) info
  summary_new=left_join(Dates_info, stats, by="Station_ID")
  
  summary_new=summary_new[!duplicated(summary_new$Station_ID), ]
  
  ## add info needed from main database file 
  data_select=data.file[,c(1:5,8)]
  data_select=data_select[!duplicated(data_select$Station_ID), ]
  
  summary_use=left_join(summary_new, data_select)
  
  #Change column order
  summary_use=setcolorder(summary_use, c(1,10:14,2:9))

  #Save each summary file
  write.csv(summary_use, newFileName)
  
}

