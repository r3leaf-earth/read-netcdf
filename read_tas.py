#############################################################
# Taken from: https://stackoverflow.com/a/66992824/9994393
# and: https://www.earthinversion.com/utilities/reading-NetCDF4-data-in-python/
#
# Summary:
#   * reads a netCDF-file into a netCDF4.dataset
# 	* finds the closest grid point for the lat-lon coordinates (50., 11.799) from a given CORDEX-netCDF file for
#     the variable tas (mean daily temperature)
#   * converts tas values in Kelvin to degrees Celsius (only the ones for the given coordinate)
#   * converts the time points from the file to python datetimes
#   * prints the grid point coordinates, and the dates and tempurates for that gridpoint, starting with:
#     Converting file to  dataset...
#     Reading lat and lon values from dataset...
#     Searching grid point for location: 50.000 11.799
#     Closest grid point found is: 50.030807 11.750615
#     2006-01-16    -6.1835 °C
#     2006-02-15    -0.2708 °C
#     2006-03-16     4.2862 °C
#     2006-04-16    10.5501 °C
#     2006-05-16    14.8754 °C
#     ...
#
# Prerequisites:
# 	* you need an .nc-file, from the CORDEX. You can download one at Copernicus' Climate Data Store
#     * create a free account. Logged in, make selections in the form below (link)
#       * monthly data is recommended for testing, since it is smaller than daily data
#       * choose variable "2m air temperature" (called 'tas' in the dataset to download)
#     * Submit the form, download the file and unzip it
#     * https://cds.climate.copernicus.eu/cdsapp#!/dataset/projections-cordex-domains-single-levels?tab=form
#	* pip install -r requirements.txt
#   * change this script, lines to change are marked with "<---"
#	  * change filename to your downloaded .nc-file
#     * change the path or place it in the same location as this script
#     * change the location to the one you are interested in (lat, lon coordinates)
#
# Usage:
# 	python read_tas.py
#
#############################################################
import os
from datetime import date, timedelta

import netCDF4
import numpy as np

# GET THE FILE
print("Converting file to dataset...")
path_to_file = os.getcwd()      # <--- change the path here, unless the .nc-file is in the same directory as this script
filename = 'tas_EUR-11_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200601-201012.nc'    # <--- change filename
dataset = netCDF4.Dataset(path_to_file + '/' + filename, 'r')

# GEO LOCATION
print("Reading lat and lon values from dataset...")
lat, lon = dataset.variables['lat'], dataset.variables['lon']

# extract lat/lon values (in degrees) to numpy arrays
latvals = lat[:]
lonvals = lon[:]


# print("lat====================================== \n", latvals)
# print("lon====================================== \n", lonvals)
#
# a function to find the index of the grid point closest to the desired location
# (in squared distance) to give lat/lon value.
def getclosest_gridpoints_indices(lats, lons, desired_lat, desired_lon):
    # find squared distance of every point on grid
    dist_sq = (lats - desired_lat) ** 2 + (lons - desired_lon) ** 2
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, lats.shape)


location_lat = 50.000       # <--- change to your desired location latitude, here
location_lon = 11.799       # <--- change to your desired location longitude, here

print("Searching grid point for location: lat: ", location_lat, ", lon: ", location_lon)
grid_lat_index, grid_lon_index = getclosest_gridpoints_indices(latvals, lonvals, location_lat, location_lon)
print("Closest grid point found is:", lat[grid_lat_index, grid_lon_index], lon[grid_lat_index, grid_lon_index])

# THE MAIN VARIABLE: TAS, TEMPERATURE

tas = dataset.variables['tas']
# Read value out of the netCDF file for temperature, all days, one location (closest grid point)
tas_k = tas[:, grid_lat_index, grid_lon_index]
# convert from degrees Kelvin to degrees Celsius
tas_degC = tas_k - 273.15

# DATE

ds_times = dataset.variables['time'][:]
# print(ds_times)

# unit of 'time' in the dataset is: days since 1949-12-01 00:00:00
# create the date_zero of the dataset as date
december_1949 = date(1949, 12, 1)


def get_time_from_dataset_as_date(index):
    days_after_1949 = ds_times[index]
    time_since_1949 = timedelta(days=days_after_1949)
    return december_1949 + time_since_1949

# PRINT DATE WITH ITS PREDICTED TEMPERATURE

for i, temperature in enumerate(tas_degC):

    time_point = get_time_from_dataset_as_date(i)
    print(time_point, "\t", '%7.4f %s' % (temperature, "°C"))

# print('%7.4f %s' % (tas_k, tas.units))
