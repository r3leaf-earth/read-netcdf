import sys

import cftime
import rioxarray
import matplotlib.pyplot as plt
import xarray

path_to_file = sys.argv[1]
xr = rioxarray.open_rasterio(path_to_file)
# xr = rioxarray.open_rasterio("../../data/hostrada/tas_1hr_HOSTRADA-v1-0_BE_gn_2023100100-2023103123.nc")
# print("\n")
# print(xr.dims)
# print("\n")
# print(xr.attrs)
# print("\n")
# print(xr.coords)
# print(xr)
# a_cftime = cftime.DatetimeProlepticGregorian(2023, 10, 1, 0, 0, 0, 0)
# print(a_cftime)

times = xr.variables['time'][:]

# times = xr['time']
print(times.__len__())


for i in times:
    # pass
    print(i)
