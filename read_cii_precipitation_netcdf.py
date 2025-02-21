import os
import sys

from netcdf_dataset_commons import DerivedDataset

# GET THE FILE
path_to_file = sys.argv[1]

# PREPARE THE DATASET
variable_name = "prAdjust"
print("Converting file to dataset using main variable " + variable_name + "...")
dataset = DerivedDataset(path_to_file, main_variable=variable_name)


# READ LOCATIONS FROM INPUT FILE (OR HARDCODE THEM HERE)
# 54.09497,13.37462 Greifswald
# 52.400882,13.055165 Potsdam
# 51.368288/12.435543 Leipzig Heiterblickstrasse 42
# 51.78195,11.14510 Harz
# 49.009452/8.400044 Karlsruhe
# 47.98036,7.90463 Freiburg???
desired_locations = [(54.09,13.37), (52.40,13.06), (51.37,12.44), (51.78,11.15), (49.01,8.40)]

# FIND CLOSEST GRID POINTS
closest_grid_indices = dataset.find_closests_grid_points_indices(desired_locations)
found_grid_points = dataset.get_many_pretty_coordinates(index_tuple_list=closest_grid_indices, decimal_places=2)

#todo replace with ennoyumerate
# for i in range(len(desired_locations)):
for i, location in enumerate(desired_locations):
    print("Searching grid point for location: ", location,
      " --> found: ", found_grid_points[i])

# READ DATA INTO DICTIONARY (for all sample addresses)
location_time_data = {}
dataset_times = dataset.get_pretty_times()
location_time_data['time'] = dataset_times

for location in found_grid_points:
    data = dataset.get_pretty_data(location)
    location_time_data[location] = data

# PREPARE LINES FOR THE OUTPUT FILE... todo> check if ennoumerate soulution form other file is faster
lines = []
coloumn_headers = ';'.join(str(a) for a in location_time_data.keys())
lines.append(coloumn_headers  + "\n")

for i in range(len(dataset_times)):
    values = []
    for key in location_time_data:

        each_locations_value = location_time_data[key][i]
        values.append(each_locations_value)
    line = ';'.join(str(a) for a in values) + "\n"
    lines.append(line)


# WRITE TO THE FILE
infile_name_with_fileextension = path_to_file.split("/")[-1]
infile_name = infile_name_with_fileextension.split(".")[0]
path_to_outfile = "out/A_"+ infile_name + ".csv"

os.makedirs(os.path.dirname(path_to_outfile), exist_ok=True)

with open(path_to_outfile, 'a+') as outfile:
    print("Writing to file ", path_to_outfile)

    outfile.write("Main Variable: " + variable_name + "\n")
    outfile.write("Name of data file: " + infile_name_with_fileextension + "\n")

    for line in lines:
        outfile.write(line)


    # for i, number_of_days in enumerate(values_for_location_rounded):
    #     year = times_as_dates[i].year
    #
    #     number_of_days_or_temperature_pretty = '%7.1f' % number_of_days
    #
    #     line = f"{year};{number_of_days_or_temperature_pretty}\n"
    #     outfile.write(line)
    #
    #     if year % 5 == 0 and year % 10 != 0:
    #         print(year, "\t", number_of_days)


# Main Variable: prAdjust
# Name of data file: 12_precipitation_bla_bla_bla_rcp85
# time; 50.0,11.8; next,loc; ...
# 1950;  503.8; 600.6; ...
# 1951;  621.7; 700.7
# 1952;  649.5; 800.8
# 1953;  695.9; 900.9
# 1954;  584.3; 500.5; ...


# unsanswered questions:
#   - what, if I want to compare 2 rcps for one location in a plot?
#     --> can someone do via excel for now
#   - when do I need objects?
#       - Dataset: main variable, rcp, time resolution (monthly...)
#       - Location: address, town, postal code, lat, lon, shortname?