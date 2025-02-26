# READ PRECIPITATION FROM CII for Europe derived from Reanalysis and Projections NETCDF ##################
#
# Works for one give location and the hardcoded variable "prAdjust". If your datafile has another variable, please change it.
#
# Summary:
#   * finds closest grid points to the location
#   * reads a netCDF-file into a netCDF4.dataset, reads location from the commandline
# 	* finds the closest grid point for the lat-lon coordinates from a given heatwaves-netCDF file
#   * uses hardcoded variable name"prAdjust"
#   * converts the time points from the file to python datetimes
#   * collects the values into a file and
#   * prints some output to stdout
#
# Dataset:
#   Climate indicators for Europe from 1940 to 2100 derived from reanalysis and climate projections
#   https://cds.climate.copernicus.eu/datasets/sis-ecde-climate-indicators/?tab=download
#
# Output:
#     Converting file to dataset...
#     Searching grid point for location:  50.0 11.0
#     Closest grid point found is: 50.0 11.0
#     prAdjust
#     reading times...
#     Writing to file  out/12_total_precipitation-projections-yearly-rcp_8_5-cclm4_8_17-mpi_esm_lr-r1i1p1-grid-v1.csv
#     1955     880.7
#     1965     707.1
#     1975     835.7
#     1985     880.0
#     ...
#     2095     1293.1

#
# Prerequisites:
#     * install the libraries you do not have yet (netCDF4, numpy, ...), e.g. by
#         * pip install -r requirements.txt
#     * you need an .nc-file from the Dataset mentioned above. You can download one at Copernicus' Climate Data Store
#         * create a free account. Logged in, make selections in the form (tab=download)
#         * Submit the form, download the file and unzip it
#	  * if you wish, change the years to be printed out
#
# Usage:
# 	python read_cds_cii_netcdf_res_point25.py /path/to/filename.nc "50.,11.799"
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
location_lat = float(coordinates[0])
location_lon = float(coordinates[1])

# print("Reading lat and lon values from dataset...")
lat, lon = dataset.variables['lat'], dataset.variables['lon']

# extract lat/lon values (in degrees) to numpy arrays
latvals = lat[:]
lonvals = lon[:]



# a function to find the index of the grid point closest to the desired location
def get_index_of_min(distances):
    return distances.argmin()
    # if distances is multidimensional, e.g. containing both lat and lon, use uravel, too
    # min_index = np.unravel_index(np.argmin(distances), distances.shape)
    # return min_index


def get_closest_gridpoints_indices(lats, lons, desired_lat, desired_lon):
    # Compute the squared differences (fast approximation)
    lat_diffs = (lats - desired_lat) ** 2
    lon_diffs = (lons - desired_lon) ** 2

    # min and index of
    lat_index = get_index_of_min(lat_diffs)
    lon_index = get_index_of_min(lon_diffs)

    return lat_index, lon_index


print("Searching grid point for location: ", location_lat, location_lon)
grid_lat_index, grid_lon_index = get_closest_gridpoints_indices(latvals, lonvals, location_lat, location_lon)
print("Closest grid point found is:", lat[grid_lat_index].round(2), lon[grid_lon_index].round(2))

variable_name = "prAdjust"
print(variable_name)

def filename_from_path(path_to_nc_file):
    filename_with_extension = path_to_nc_file.split("/")[-1]
    filename = filename_with_extension.split(".")[0]
    return filename

infile_name = filename_from_path(path_to_file)

#path_to_outfile = "out/"+ variable_name+ "_" + infile_name + ".csv"
path_to_outfile = "out/"+ infile_name + ".csv"

# HWD_EU_climate(time,lat,lon)

values = dataset.variables[variable_name][:]
values_for_location_many_decimal_places = values[:, grid_lat_index, grid_lon_index].compressed()
values_for_location_rounded = values_for_location_many_decimal_places.round(1)
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

os.makedirs(os.path.dirname(path_to_outfile), exist_ok=True)

with open(path_to_outfile, 'a+') as outfile:
    print("Writing to file ", path_to_outfile)
    if is_newfile:
        # write column headers
        outfile.write(str(location_lat) + "," + str(location_lon) + "\n")
        outfile.write("time; " + variable_name + "\n")

    for i, number_of_days in enumerate(values_for_location_rounded):
        year = times_as_dates[i].year

        number_of_days_or_temperature_pretty = '%7.1f' % number_of_days

        line = f"{year};{number_of_days_or_temperature_pretty}\n"
        outfile.write(line)

        if year % 5 == 0 and year % 10 != 0:
            print(year, "\t", number_of_days)
