import sys
import netCDF4

# Recommendation:
#    Run this module interactively with `python -i explore_netCDF_dataset.py YOUR_DATASET.nc`
#    In the shell, you can then use dataset.variables, etc.

# GET THE FILE

path_to_file = sys.argv[1]
print("Converting file to dataset...")
dataset = netCDF4.Dataset(path_to_file, 'r')
print("Dataset: ", dataset)
#print("Dimensions:", dataset.dimensions.keys())
#print("Variables: ", dataset.variables.keys())
print("\n")

# print(dataset.variables.values())

#For info on a single variable, e.g "time" use
#`>>> dataset.variables['time']`
