
# Paper title: A global dataset of surface water and groundwater salinity measurements from 1980-2019
# Data citation: Thorslund, Josefin; van Vliet, Michelle T H (2020): A global salinity dataset of surface water and groundwater measurements from 1980-2019. PANGAEA, https://doi.pangaea.de/10.1594/PANGAEA.913939 

# Data set creator:  Josefin Thorslund - Stockholm University & Utrecht University
# Data set creator:  Michelle van Vliet - Utrecht University

#################################################################################################################

# Clear console and list
rm(list=ls())
cat("\014") 

# Set working directory and load packages
setwd("") #choose your file location

#Load packages and functions 
require(data.table)
require(dplyr)
require(ggplot2)
require(sjPlot)
require(rworldmap)


#Theme used for all Figures
My_graph_theme_large = theme(
  axis.title.x = element_text(size = 20,face="bold", color="Black", vjust=-0.5),
  axis.text.x = element_text(size = 20, face="bold",color="Black"),
  axis.title.y = element_text(size = 20,face="bold",color="Black", margin = margin(t = 0, r = 20, b = 0, l = 0)),
  axis.text.y = element_text(size = 20, face="bold",color="Black"),
  legend.title = element_text(size = 20, face="bold",color="Black"),
  legend.text = element_text(size = 20, face="bold",color="Black"))



#### Load data 

## Groundwater data
Gw_all=fread('Groundwaters_database.csv') 
Gw_summary=fread('Groundwaters_summary.csv') 

## River data
Rivers_all=fread('Rivers_database.csv') 
Rivers_summary=fread('Rivers_summary.csv')

## Lake/Reservoir data
Lakes_all=fread('Lakes_Reservoirs_database.csv')
Lakes_summary=fread('Lakes_Reservoirs_summary.csv')

ALL_DATA=rbind(Gw_all, Rivers_all, Lakes_all, fill=TRUE)

# Structure of the data, replace for each dataset to view 
str(ALL_DATA)                            


#################################################
######### Data processing for figure 1 ##########
#################################################

### Station count by continent and water type 

count=ALL_DATA[Date>="1980-01-01" & Date<="2019-12-31",
               list(station_count=length(unique(Station_ID)))
               ,by=list(Continent=Continent, Water_type=Water_type)]

All_wt_count=count[,list(total=sum(station_count))
                       ,by=list(Continent=Continent, Water_type=Water_type)]


All_data_select=ALL_DATA[,c(1,2,3,4,5,6,7,12)] #needed columns for figure

# extract world map info
world = map_data("world")
names(world)

#Rename region to Country
world = rename(world, Country = region)

#1980s stats (Fig. 1a-b)
Stats=All_data_select[Date>="1980-01-01" & Date<="1989-12-31",
                  list(station_count=length(unique(Station_ID)))
                  ,by=list(Country=Country)]

Stats$Period="1980s"

#Save 
fwrite(Stats, 'Eighties_station_count.csv') 

#1990s
Stats=All_data_select[Date>="1990-01-01" & Date<="1999-12-31",
                  list(station_count=length(unique(Station_ID)))
                  ,by=list(Country=Country)]

Stats$Period="1990s"
fwrite(Stats, 'Nineties_station_count.csv') 

#2000s
Stats=All_data_select[Date>="2000-01-01" & Date<="2019-12-31",
                  list(station_count=length(unique(Station_ID)))
                  ,by=list(Country=Country)]

Stats$Period="2000s"
fwrite(Stats, 'Twenties_station_count.csv') 


## Full data period
Stats=All_data_select[Date>="1980-01-01" & Date<="2019-12-31",
                  list(station_count=length(unique(Station_ID)))
                  ,by=list(Country=Country)]

Stats$Period="global"
fwrite(Stats, 'Global_station_count.csv') 


###### Function that plots all decadal data stats on global map (Fig. 1a-b)

fileNames = c("Eighties_station_count.csv", "Nineties_station_count.csv", "Twenties_station_count.csv", "Global_station_count.csv")
extension <- "csv"
fileNumbers <- seq(fileNames)

for (fileNumber in fileNumbers) {
  
  newFileName <-  paste("Fig_1_", 
                        fileNames[fileNumber])
  
  #Read files 
  Data=fread(fileNames[fileNumber])

#Create categories and plot station counts within these ranges
Data$Amount=cut(Data$station_count, breaks = c(0, 100, 500,1000,5000, 10000, 1000000))


# Join data to global map
myMap <- joinCountryData2Map(Data, joinCode = "NAME",
                              nameJoinColumn = "Country", mapResolution = "high")

#save as jpeg with resolution of 600 dpi
jpeg(paste(newFileName,".jpg",sep=""), width = 6, height = 4, units = 'in', res = 600)

}

############  Bar chart of sampled water types, per decade (Fig. 1c) 

GW_single=Gw_all[!duplicated(Gw_all$Station_ID), ]
River_single=Rivers_all[!duplicated(Rivers_all$Station_ID), ]
Lake_single=Lakes_all[!duplicated(Lakes_all$Station_ID), ]
All_wt=rbind(GW_single, River_single, Lake_single, fill=TRUE)

#1980s
All_wt_count=All_wt[Date>="1980-01-01" & Date<="1989-12-31"
                    ,list(station_count=length(Station_ID))
                    ,by=list(Water_type=Water_type, Continent=Continent)]

All_wt_count_new=All_wt_count[,list(total=sum(station_count))
                              ,by=list(Continent=Continent)]

ALL_stats=merge(All_wt_count, All_wt_count_new, by="Continent")  


ALL_stats$percent=(ALL_stats$station_count/ALL_stats$total)*100

Global_stats=All_wt[Date>="1980-01-01" & Date<="1989-12-31"
                    ,list(station_count=length(Station_ID))
                    ,by=list(Water_type=Water_type)]

Global_stats$total=Global_stats[,list(total=sum(station_count))]
Global_stats$Continent="Global"
Global_stats$percent=(Global_stats$station_count/Global_stats$total)*100
ALL_stats=rbind(ALL_stats,Global_stats)

write.csv(ALL_stats, 'water_type_by_continent_1980s.csv')

#1990s
All_wt_count=All_wt[Date>="1990-01-01" & Date<="1999-12-31"
                    ,list(station_count=length(Station_ID))
                    ,by=list(Water_type=Water_type, Continent=Continent)]

All_wt_count_new=All_wt_count[,list(total=sum(station_count))
                              ,by=list(Continent=Continent)]

ALL_stats=merge(All_wt_count, All_wt_count_new, by="Continent")  
ALL_stats$percent=(ALL_stats$station_count/ALL_stats$total)*100

Global_stats=All_wt[Date>="1990-01-01" & Date<="1999-12-31"
                    ,list(station_count=length(Station_ID))
                    ,by=list(Water_type=Water_type)]

Global_stats$total=Global_stats[,list(total=sum(station_count))]
Global_stats$Continent="Global"
Global_stats$percent=(Global_stats$station_count/Global_stats$total)*100
ALL_stats=rbind(ALL_stats,Global_stats)

write.csv(ALL_stats, 'water_type_by_continent_1990s.csv')

#2000s
All_wt_count=All_wt[Date>="2000-01-01" & Date<="2019-12-31"
                    ,list(station_count=length(Station_ID))
                    ,by=list(Water_type=Water_type, Continent=Continent)]

All_wt_count_new=All_wt_count[,list(total=sum(station_count))
                              ,by=list(Continent=Continent)]

ALL_stats=merge(All_wt_count, All_wt_count_new, by="Continent")  

ALL_stats$percent=(ALL_stats$station_count/ALL_stats$total)*100

Global_stats=All_wt[Date>="2000-01-01" & Date<="2019-12-31"
                    ,list(station_count=length(Station_ID))
                    ,by=list(Water_type=Water_type)]

Global_stats$total=Global_stats[,list(total=sum(station_count))]
Global_stats$Continent="Global"
Global_stats$percent=(Global_stats$station_count/Global_stats$total)*100
ALL_stats=rbind(ALL_stats,Global_stats)

write.csv(ALL_stats, 'water_type_by_continent_2000s.csv')


#### Function that plots each decadal stats

fileNames = c("water_type_by_continent_1980s.csv", "water_type_by_continent_1990s.csv", "water_type_by_continent_2000s.csv")
extension <- "csv"
fileNumbers <- seq(fileNames)

for (fileNumber in fileNumbers) {
  
  newFileName <-  paste("Fig_1c_", 
                        fileNames[fileNumber])
  
  #Read files 
  Data=fread(fileNames[fileNumber])
  
  Data$Continent=as.factor(Data$Continent)
  levels(Data$Continent)
  
  # Change order of continents 
  Data$Continent = factor(Data$Continent,levels(Data$Continent)[c(6,2,1,3,7,5,4)])
  levels(Data$Continent)
  
  
  p <- ggplot(Data, aes(x=Continent, y=percent, fill=Water_type)) 
  plot=p + geom_bar(stat="identity") + 
    xlab("") +  ylab("Percent of total") + theme_bw() + coord_flip() +
    guides(fill = guide_legend(
      keywidth = 0.7, keyheight = 0.7, 
      reverse=F, title.position="top", 
      nrow = 3, byrow=T)) +
    theme(legend.position="bottom") 
  
  barplot=plot+My_graph_theme_large+scale_fill_manual(values=c("gray78", "gray2", "grey28", "white"))
  
  #save as svg
  svg(paste(newFileName,".svg",12*2,9*2))
}

#############  Violin plot per decade (Fig. 1d) 

## 1980s
Stats_global=All_data_select[Date>="1980-01-01" & Date<="1989-12-31",
                      list(measurement_count=length(EC))
                      ,by=list(Station_ID=Station_ID, Water_type=Water_type)]

Stats_global$measurement_count=as.numeric(Stats_global$measurement_count)
Stats_global$Continent="Global"

violinplot=ggplot(Stats_global, aes(x=Water_type, y=measurement_count, fill=Water_type)) + 
  geom_violin(na.rm=TRUE) + scale_y_log10()+My_graph_theme_large+scale_fill_manual(values=c("gray78", "gray2", "gray53"))
violinplot=violinplot + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                              panel.background = element_blank(), axis.line = element_line(colour = "black"))

pdf("violin_plot_1980s.PDF",16*2,9*2)
print(violinplot) #When the plot is stored as an object (as defined in row 35), need to add it again below to plot it
dev.off()


### 1990s
Stats_global=All_data_select[Date>="1990-01-01" & Date<="1999-12-31",
               list(measurement_count=length(EC))
               ,by=list(Station_ID=Station_ID, Water_type=Water_type)]

Stats_global$measurement_count=as.numeric(Stats_global$measurement_count)
Stats_global$Continent="Global"

violinplot=ggplot(Stats_global, aes(x=Water_type, y=measurement_count, fill=Water_type)) + 
  geom_violin(na.rm=TRUE) + scale_y_log10()+My_graph_theme_large+scale_fill_manual(values=c("gray78", "gray2", "gray53"))
violinplot=violinplot + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                              panel.background = element_blank(), axis.line = element_line(colour = "black"))

pdf("violin_plot_1990s.PDF",16*2,9*2)
print(violinplot) #When the plot is stored as an object (as defined in row 35), need to add it again below to plot it
dev.off()


## 2000s
Stats_global=All_data_select[Date>="2000-01-01" & Date<="2019-12-31",
                      list(measurement_count=length(EC))
                      ,by=list(Station_ID=Station_ID, Water_type=Water_type)]

Stats_global$measurement_count=as.numeric(Stats_global$measurement_count)
Stats_global$Continent="Global"

violinplot=ggplot(Stats_global, aes(x=Water_type, y=measurement_count, fill=Water_type)) + 
  geom_violin(na.rm=TRUE) + scale_y_log10()+My_graph_theme_large+scale_fill_manual(values=c("gray78", "gray2", "gray53"))
violinplot=violinplot + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                              panel.background = element_blank(), axis.line = element_line(colour = "black"))

pdf("violin_plot_2000s.PDF",16*2,9*2)
print(violinplot) 
dev.off()

######################################################################################################