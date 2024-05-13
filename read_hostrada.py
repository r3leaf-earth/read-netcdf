#############################################################
# Taken from: https://stackoverflow.com/a/66992824/9994393
# and: https://www.earthinversion.com/utilities/reading-NetCDF4-data-in-python/
#
# Summary:
#   * reads a netCDF-file into a netCDF4.dataset
#   * reads the main climate variable from the file name due to Hostrada standard file names
# 	* finds the closest grid point for the lat-lon coordinates (50., 11.799)
#   * reads the climate variable for the grid point
#   * reads the dataset's time points and converts them to datetimes
#   * writes time and climate variable into a csv-file, separator ";", e.g.
#     * outfile: out/hostrada.csv , climate variable: uhi
#         time;uhi
#         2023-09-01 00:00:00;2.0
#         2023-09-01 01:00:00;2.1
#         2023-09-01 02:00:00;2.1
#         2023-09-01 03:00:00;2.2
#         2023-09-01 04:00:00;2.1
#         2023-09-01 05:00:00;1.9
#         2023-09-01 06:00:00;1.7
#         2023-09-01 07:00:00;1.4
#         2023-09-01 08:00:00;1.0
#         2023-09-01 09:00:00;0.7
#         ...
#
# Prerequisites:
#   * a file from HOSTRADA: https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/hostrada/
#     * has been downloaded
#     * which has not been renamed
#   * geocoordinates have been changed to your desired location in Germany (hostrada is for Gemany only)
#
#
# Usage:
#   * see README for how to install requirements and venv
#   * run with replaced path to downloaded HOSTRADA file
#     `python read_hostrada.py "path/to/uhi_1hr_HOSTRADA-v1-0_BE_gn_2023050100-2023053123.nc"`
#   * see csv file and if you want, plot it with `python plot_hostrada_from_csv.py`
#
# NOTE:
#  * if you do not rename your outfile, this script will append to it (if it exists)
#  * this is desired behavior. It is used for accumulating more than one month (the hostrada files are per month)
#    into one output file. This way you could, for exaple, plot a whole year from one csv file later.
#
#############################################################
import os.path
import sys

import netCDF4
import numpy as np

# TO BE CHANGED BY USER, IF DESIRED
path_to_outfile = "out/hostrada.csv"

location_lat = 51.35618  # <--- change to your desired location latitude, here
location_lon = 12.41687  # <--- change to your desired location longitude, here

# Berlin Alexanderplatz 52.52165/13.41144
# Cologne 50.9380/6.9572
# Leipzig Loebauer 51.35618/12.41687


# GET THE FILE
path_to_file = sys.argv[1]
print("Converting file to dataset...")
dataset = netCDF4.Dataset(path_to_file, 'r')


def climate_variable_name_from_path_to_file(path_to_file):
    filename = path_to_file.split("/")[-1]
    words_in_filename = filename.split("_")
    return words_in_filename[0]


# THE MAIN VARIABLE
climate_variable_name = climate_variable_name_from_path_to_file(path_to_file)
print("Main variable name is: ", climate_variable_name)
climate_variable = dataset.variables[climate_variable_name]

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


print("Searching grid point for location: lat: ", location_lat, ", lon: ", location_lon)
grid_lat_index, grid_lon_index = getclosest_gridpoints_indices(latvals, lonvals, location_lat, location_lon)
print("Closest grid point found is:", lat[grid_lat_index, grid_lon_index], lon[grid_lat_index, grid_lon_index])

# CLIMATE VARIABLE
# Read value out of the netCDF file for temperature*, all days, one location (closest grid point)
# *temperature or another climate variable
print("...for found gridpoint...")
climate_variable_for_location = climate_variable[:, grid_lat_index, grid_lon_index]

# DATE
print("reading times...")
ds_times = dataset.variables['time']
times_as_dates = netCDF4.num2date(ds_times[:], ds_times.units, ds_times.calendar)


# WRITE TO FILE (or PRINT) DATE WITH ITS PREDICTED TEMPERATURE (or other climate variable)
# if newfile write header, therefore:
exists = os.path.exists(path_to_outfile)
is_newfile = not exists

with open(path_to_outfile, 'a+') as outfile:
    print("Writing to file ", path_to_outfile)
    if is_newfile:
        # write column headers
        outfile.write("time;" + climate_variable_name + "\n")

    for i, climate_var in enumerate(climate_variable_for_location):
        time_point = times_as_dates[i]
        # print(time_point, "\t", '%7.4f %s' % (temperature, "°C"))

        climate_var = round(climate_var, 1)
        datetime_climateVar = f"{time_point};{climate_var}\n"
        #print(datetime_temperature)
        outfile.write(datetime_climateVar)
