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
import os

import netCDF4
import numpy as np

# TO BE CHANGED BY USER, IF DESIRED
path_to_outfile = "out/cordex.csv"

location_lat = 50.000  # <--- change to your desired location latitude, here
location_lon = 11.799  # <--- change to your desired location longitude, here

# GET THE FILE
print("Converting file to dataset...")
path_to_file = os.getcwd()  # <--- change the path here, unless the .nc-file is in the same directory as this script
filename = 'tas_EUR-11_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200601-201012.nc'  # <--- change filename
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


print("Searching grid point for location: lat: ", location_lat, ", lon: ", location_lon)
grid_lat_index, grid_lon_index = getclosest_gridpoints_indices(latvals, lonvals, location_lat, location_lon)
print("Closest grid point found is:", lat[grid_lat_index, grid_lon_index], lon[grid_lat_index, grid_lon_index])

# THE MAIN VARIABLE: TAS, TEMPERATURE
# TODO: read main variable from file name as in hostrada and heatwaves scipts
tas = dataset.variables['tas']
# Read value out of the netCDF file for temperature, all days, one location (closest grid point)
tas_k = tas[:, grid_lat_index, grid_lon_index]
# convert from degrees Kelvin to degrees Celsius
tas_degC = tas_k - 273.15

# DATE
print("reading times...")
ds_times = dataset.variables['time']
times_as_dates = netCDF4.num2date(ds_times[:], ds_times.units, ds_times.calendar)

# print(times_as_dates)


# WRITE TO FILE (or PRINT) DATE WITH ITS PREDICTED TEMPERATURE (or other climate variable)
# if newfile write header, therefore:
exists = os.path.exists(path_to_outfile)
is_newfile = not exists

os.makedirs(os.path.dirname(path_to_outfile), exist_ok=True)

with open(path_to_outfile, 'a+') as outfile:
    print("Writing to file ", path_to_outfile)
    if is_newfile:
        # write column headers
        outfile.write("time; " + "tas [°C]" + "\n")

    for i, climate_var in enumerate(tas_degC):
        time_point = times_as_dates[i]
        climate_var = round(climate_var, 1)

        datetime_climateVar = '%s %s %7.1f %s' % (time_point, "; ", climate_var, "\n")
        # print(datetime_climateVar)
        outfile.write(datetime_climateVar)


# print('%7.4f %s' % (tas_k, tas.units))
