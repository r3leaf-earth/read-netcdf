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
# Prerequisites & Usage see README.md
#
#############################################################
import sys
from datetime import date, timedelta, datetime
import netCDF4
import numpy as np


# GET THE FILE

path_to_file = sys.argv[1]
print("Converting file to dataset...")
dataset = netCDF4.Dataset(path_to_file, 'r')

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


location_lat = 51.35618      # <--- change to your desired location latitude, here
location_lon = 12.41687      # <--- change to your desired location longitude, here

# Berlin Alexnderplatz 52.52165/13.41144
# Cologne 50.9380/6.9572
# Leipzig Loebauer  51.35618/12.41687

print("Searching grid point for location: lat: ", location_lat, ", lon: ", location_lon)
grid_lat_index, grid_lon_index = getclosest_gridpoints_indices(latvals, lonvals, location_lat, location_lon)
print("Closest grid point found is:", lat[grid_lat_index, grid_lon_index], lon[grid_lat_index, grid_lon_index])

# THE MAIN VARIABLE
filename = path_to_file.split("/")[-1]
words_in_filename = filename.split("_")
climate_variable_name = words_in_filename[0]

print("Main variable name is: ", climate_variable_name)
climate_variable = dataset.variables[climate_variable_name]
# Read value out of the netCDF file for temperature, all days, one location (closest grid point)
print("...for found gridpoint...")
climate_variable_for_location = climate_variable[:, grid_lat_index, grid_lon_index]

# DATE
print("reading times...")
ds_times = dataset.variables['time']
times_as_dates = netCDF4.num2date(ds_times[:], ds_times.units, ds_times.calendar)


# PRINT DATE WITH ITS PREDICTED TEMPERATURE AND WRITE TO FILE

with open("out/hostrada.csv", 'a+') as outfile:
    # outfile.write("time;" + climate_variable_name + "\n")

    for i, climate_var in enumerate(climate_variable_for_location):

        time_point = times_as_dates[i]
        # print(time_point, "\t", '%7.4f %s' % (temperature, "°C"))

        climate_var = round(climate_var, 1)
        datetime_climateVar = f"{time_point};{climate_var}\n"
        #print(datetime_temperature)
        outfile.write(datetime_climateVar)



# print('%7.4f %s' % (tas_k, tas.units))

