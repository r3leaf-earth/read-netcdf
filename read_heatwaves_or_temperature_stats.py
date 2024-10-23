# READ HEATWAVES NETCDF ##################
#
# Note: Works for .nc-files from both "Heat waves and cold spells in Europe derived from climate projections" and
#       "Temperature statistics for Europe derived from climate projections"
#
# Summary:
#   * reads a netCDF-file into a netCDF4.dataset
# 	* finds the closest grid point for the lat-lon coordinates from a given heatwaves-netCDF file
#	* reads the variable, e.g. HWD_EU_climate, heatwave days in the climate definition of a heat day
#   * converts the time points from the file to python datetimes
#   * prints the desired coordinates and their closest grid point
#   * prints the variable, e.g. HWD_EU_climate
#   * prints the years with their respective number of heat days, prints for years ending in a 5 
#
# Output:
#    Converting file to dataset...
#    Searching grid point for location: lat:  50.0 , lon:  11.799
#    Closest grid point found is: 50.0 11.8
#    HWD_EU_climate
#    1995 	 1.5
#    2005 	 2.1
#    2015 	 2.9
#    2025 	 2.6
#    ...	 ...
#    2085 	 5.1
#
# Prerequisites:
#     * install the libraries you do not have yet (netCDF4, numpy, ...)
#     * you need an .nc-file, from "Heat Waves and Cold Spells". You can download one at Copernicus' Climate Data Store
#     * create a free account. Logged in, make selections in the form below (link)
#     * Submit the form, download the file and unzip it
#     * https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-heat-and-cold-spells?tab=form
#     * change this script
#         * change the location to the one you are interested in (lat, lon coordinates)
#	  * if you wish, change the years to be printed out
#
# Usage:
# 	python read_heatwaves_or_temperature_stats.py /path/to/HWD_EU_end_of_filename.nc "50.,11.799"
#
#############################################################
import os
import sys

import netCDF4
import numpy as np

# GET THE FILE

path_to_file = sys.argv[1]
print("Converting file to dataset...")
dataset = netCDF4.Dataset(path_to_file, 'r')

# # GEO LOCATION

coordinates = sys.argv[2].split(',')
location_lat = float(coordinates[0])  # <--- change to your desired location latitude, here
location_lon = float(coordinates[1])  # <--- change to your desired location longitude, here

# print("Reading lat and lon values from dataset...")
lat, lon = dataset.variables['lat'], dataset.variables['lon']
#
# extract lat/lon values (in degrees) to numpy arrays
latvals = lat[:]
lonvals = lon[:]


# print("lat====================================== \n", latvals)
# print("lon====================================== \n", lonvals)


# a function to find the index of the grid point closest to the desired location
def getclosest_gridpoints_indices(lats, lons, desired_lat, desired_lon):
    # given lat, round
    grid_lat = np.round(desired_lat, 1)
    grid_lon = np.round(desired_lon, 1)

    index_lat = lats.searchsorted(grid_lat)
    index_lon = lons.searchsorted(grid_lon)

    return index_lat, index_lon


print("Searching grid point for location: ", location_lat, location_lon)
grid_lat_index, grid_lon_index = getclosest_gridpoints_indices(latvals, lonvals, location_lat, location_lon)
print("Closest grid point found is:", lat[grid_lat_index].round(1), lon[grid_lon_index].round(1))


def climate_variable_name_from_filename(path_to_nc_file):
    filename_with_extension = path_to_nc_file.split("/")[-1]
    filename = filename_with_extension.split(".")[0]
    words_in_filename = filename.split("_")
    climate_variable_name = "_".join(words_in_filename[0:3])
    return filename, climate_variable_name


infile_name, variable_name = climate_variable_name_from_filename(path_to_file)
print(variable_name)
path_to_outfile = "out/heatwaves_or_temp_stats_" + infile_name + ".csv"

# HWD_EU_climate(time,lat,lon)

heat = dataset.variables[variable_name][:]
heat_days_many_decimal_places = heat[:, grid_lat_index, grid_lon_index].compressed()
heat_days = heat_days_many_decimal_places.round(1)
# print(heat_days)

# DATE
print("reading times...")
ds_times = dataset.variables['time']
times_as_dates = netCDF4.num2date(ds_times[:], ds_times.units, ds_times.calendar)
# print(times_as_dates[2].year)

# WRITE TO FILE (or PRINT) DATE WITH ITS PREDICTED TEMPERATURE (or other climate variable)
# if newfile write header, therefore:
exists = os.path.exists(path_to_outfile)
is_newfile = not exists

with open(path_to_outfile, 'a+') as outfile:
    print("Writing to file ", path_to_outfile)
    if is_newfile:
        # write column headers
        outfile.write("time; " + variable_name + "\n")

    for i, number_of_days in enumerate(heat_days):
        year = times_as_dates[i].year

        number_of_days_or_temperature_pretty = '%7.1f' % number_of_days

        line = f"{year};{number_of_days_or_temperature_pretty}\n"
        outfile.write(line)

        if year % 5 == 0 and year % 10 != 0:
            print(year, "\t", number_of_days)
