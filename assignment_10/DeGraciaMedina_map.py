# %%
# Import the necessary tools
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
import fiona
import contextily as ctx
from shapely.geometry import Point

# %%
# Gauges II USGS stream gauge dataset:
# Download here:
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder
# Link used: https://water.usgs.gov/GIS/dsdl/gagesII_9322_point_shapefile.zip
# Reading it using geopandas
file = os.path.join('../data/gagesII_9322_point_shapefile',
                    'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# %%

# The variable "file" will automatically join the address of your shapefile.
print('The current work directory is:')
print(os.getcwd())
print()
print('The data is storaged at:')
print(file)
print()

# This shows if the path exists or not, to check if there is any problem
# finding the data. "True" means it's ok. "False" means there is a problem.
print('Is everything ok with the path to start working now?')
os.path.exists(file)

# %%
# Let look at what this is
type(gages)
gages.head()
gages.columns
gages.shape

# Looking at the geometry now
gages.geom_type
# check our CRS - coordinate reference system
gages.crs
# Check the spatial extent
gages.total_bounds
# NOTE to selves - find out how to get these all at once

# %%
# Now lets make a map!
fig, ax = plt.subplots(figsize=(5, 5))
gages.plot(ax=ax)
plt.show()

# Zoom  in and just look at AZ
gages.columns
gages.STATE.unique()
gages_AZ = gages[gages['STATE'] == 'AZ']
gages_AZ.shape

# More advanced plot of AZ gages - color by attribute
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=45, cmap='OrRd',
              ax=ax)
ax.set_title("Arizona stream gauge drainge area\n (sq km)")
plt.show()

# %%
# Adding more datasets
# https://www.usgs.gov/core-science-systems/ngp/national-hydrography/\
# access-national-hydrography-products
# Final link used: https://prd-tnm.s3.amazonaws.com/StagedProducts/\
#                  Hydrography/WBD/HU2/GDB/WBD_15_HU2_GDB.zip

# HUC means: Hydrologic Unit Code
# Reading in a geodataframe
# Watershed boundaries for the lower Colorado. Polygon layer.
file = os.path.join('../data/WBD_15_HU2_GDB', 'WBD_15_HU2_GDB.gdb')
os.path.exists(file)
fiona.listlayers(file)
HUC6 = gpd.read_file(file, layer="WBDHU6")

type(HUC6)
HUC6.head()

# plot the new layer we got:
fig, ax = plt.subplots(figsize=(5, 5))
HUC6.plot(ax=ax)
ax.set_title("HUC Boundaries")
plt.show()

# Showing the Coordinate Reference System and the Total Bounds
HUC6.crs
HUC6.total_bounds

# %%
# Add some points
# UofA:  32.22877495, -110.97688412
# Verde River Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-110.97688412, 32.22877495],
                       [-111.7891667, 34.44833333]])

# make these into spatial features
point_geom = [Point(xy) for xy in point_list]
point_geom

# mape a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HUC6.crs)

# plot these on the first dataset
# Then we can plot just one layer at a time
fig, ax = plt.subplots(figsize=(5, 5))
HUC6.plot(ax=ax)
point_df.plot(ax=ax, color='red', marker='x', markersize=50)
ax.set_title("HUC Boundaries")
plt.show()

# %%
# Now trying to put it all together - adding our two points to the stream gages
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False, legend=True,
              markersize=45, cmap='Set2', ax=ax)
point_df.plot(ax=ax, color='r', marker='x', markersize=50)

# Trouble!! we are in two differnt CRS
gages_AZ.crs
point_df.crs

# To fix this we need to re-project
points_project = point_df.to_crs(gages_AZ.crs)

# Trying to plot again
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=45, cmap='Set2',
              ax=ax)
points_project.plot(ax=ax, color='r', marker='x', markersize=50)
# NOTE: .to_crs() will only work if your original spatial object has a CRS \
# assigned
# to it AND if that CRS is the correct CRS!

# %%
# Xenia
# From:https://www.epa.gov/eco-research/ecoregion-download-files-state-region-9

# Ecoregions of Arizona. Polygon layer.
file = os.path.join('../data/az_eco_l3', 'az_eco_l3.shp')
os.path.exists(file)
fiona.listlayers(file)
eco_AZ = gpd.read_file(file, layer="az_eco_l3")

type(eco_AZ)
eco_AZ.head()

# More advanced - color by attribute
fig, ax = plt.subplots(figsize=(5, 5))
eco_AZ.plot(column='NA_L2NAME', categorical=True, legend=True, cmap='YlGn',
            ax=ax)
ax.set_title("Ecoregions of Arizona")
plt.show()

# Reviewing the Coordinate Reference System
eco_AZ.crs
# Changing all the layers to the same CRS as "Gages" layer.
eco_AZ_project = eco_AZ.to_crs(gages_AZ.crs)

# %%
# Xenia
# From: https://data.fs.usda.gov/geodata/edw/datasets.php?xmlKeyword=arizona

# Temperatures of Arizona. Point layer.
file = os.path.join('../data/S_USA.NorWeST_TemperaturePoints.gdb',
                    'S_USA.NorWeST_TemperaturePoints.gdb')
os.path.exists(file)
fiona.listlayers(file)
temp_AZ = gpd.read_file(file, layer="NorWeST_TemperaturePoints")

type(temp_AZ)
temp_AZ.head()

# More advanced - color by attribute
fig, ax = plt.subplots(figsize=(5, 5))
temp_AZ.plot(categorical=True, legend=True, cmap='RdYlBu', ax=ax)
ax.set_title("Temperatures of Arizona")
plt.show()

# Reviewing the Coordinate Reference System
temp_AZ.crs
# Changing all the layers to the same CRS as "Gages" layer.
temp_AZ_project = temp_AZ.to_crs(gages_AZ.crs)

# %%
# Xenia
# From: http://repository.azgs.az.gov/category/thematic-keywords/geodatabase

# Wildfires of Arizona. Point layer.
file = os.path.join('../data/azwildfires_di44_v1.gdb_',
                    'AZWildfires_DI44_v1.gdb')
os.path.exists(file)
fiona.listlayers(file)
fires_AZ = gpd.read_file(file, layer="RainGages_AZFires")

type(fires_AZ)
fires_AZ.head()

# More advanced - color by attribute
fig, ax = plt.subplots(figsize=(5, 5))
fires_AZ.plot(categorical=True, legend=True, cmap='OrRd', ax=ax)
ax.set_title("Wildfires of Arizona")
plt.show()

# Reviewing the Coordinate Reference System
fires_AZ.crs
# Changing all the layers to the same CRS as "Gages" layer.
fires_AZ_project = fires_AZ.to_crs(gages_AZ.crs)

# %%
# now putting everything on the plot:

# Changing all the layers to the same CRS as "Gages" layer.
HUC6_project = HUC6.to_crs(gages_AZ.crs)

# Now plot
# Adding each layer to the map
fig, ax = plt.subplots(figsize=(10, 5))
eco_AZ_project.plot(column='NA_L2NAME', categorical=True, legend=True,
                    label='Ecoregions', cmap='YlGn', ax=ax)
gages_AZ.plot(categorical=False, legend=True,
              label='Stream Gages', markersize=15, cmap='ocean', ax=ax)
temp_AZ_project.plot(categorical=False, legend=True, markersize=15, marker='>',
                     cmap='RdYlBu', ax=ax, label='Temperature')
fires_AZ_project.plot(categorical=False, legend=True, marker='^',
                      markersize=80, cmap='Reds', ax=ax, label='Wildfires')
points_project.plot(ax=ax, legend=True, label='Points of interest',
                    color='red', marker='x', markersize=80, linewidth=2)
HUC6_project.boundary.plot(ax=ax, color=None, edgecolor='black', linewidth=0.5)

# Making zoom to the bounds of the prefered layer. In this case Eco-regions.
xlim = ([eco_AZ_project.total_bounds[0],  eco_AZ_project.total_bounds[2]])
ylim = ([eco_AZ_project.total_bounds[1],  eco_AZ_project.total_bounds[3]])
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set(title='Flow Gages, Ecoregions, Temperature \n Arizona State',
       xlabel='Longitude', ylabel='Latitude')

# Show the legend
ax.legend()

# Show the plot
plt.show()

# %%
