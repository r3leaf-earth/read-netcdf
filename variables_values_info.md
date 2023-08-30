# Varibles, Units, Ranges 

## Dimensions

```python
>>> dataset.dimensions.keys()
dict_keys(['time', 'rlat', 'rlon', 'bnds', 'vertices'])
```


## Variables (include dimensions)
```python
>>> dataset.variables.keys()
dict_keys(['time', 'time_bnds', 'rlat', 'rlon', 'rotated_latitude_longitude', 
           'lat', 'lon', 'lat_vertices', 'lon_vertices', 'height', 'tas'])
```

For info on a single variable, e.g "tas" use
`>>> dataset.variables['tas']`


## Details on all variables
Definition and ranges of variables in file obtained by
    print(dataset.variables.values())

dict_values([<class 'netCDF4._netCDF4.Variable'>

TIME
    float64 time(time)
        bounds: time_bnds
        axis: T
        long_name: time
        standard_name: time
        units: days since 1949-12-01 00:00:00
        calendar: proleptic_gregorian
    unlimited dimensions: time
    current shape = (60,)
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>

TIME_BNDS
    float64 time_bnds(time, bnds)
    unlimited dimensions: time
    current shape = (60, 2)
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>
    float64 rlat(rlat)
        units: degrees
        axis: Y
        long_name: latitude in rotated pole grid
        standard_name: grid_latitude
    unlimited dimensions:
    current shape = (412,)
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>

RLAT
    float64 rlat(rlat)
        units: degrees
        axis: Y
        long_name: latitude in rotated pole grid
        standard_name: grid_latitude
    unlimited dimensions:
    current shape = (412,)
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>

RLON
    float64 rlon(rlon)
        units: degrees
        axis: X
        long_name: longitude in rotated pole grid
        standard_name: grid_longitude
    unlimited dimensions:
    current shape = (424,)
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>

ROTATED_LATITUDE_LONGITUDE
    int32 rotated_latitude_longitude()
        grid_mapping_name: rotated_latitude_longitude
        grid_north_pole_latitude: 39.25
        grid_north_pole_longitude: -162.0
        north_pole_grid_longitude: 0.0
    unlimited dimensions:
    current shape = ()
    filling on, default _FillValue of -2147483647 used, <class 'netCDF4._netCDF4.Variable'>

LAT
    float32 lat(rlat, rlon)
        standard_name: latitude
        long_name: latitude coordinate
        units: degrees_north
        bounds: lat_vertices
    unlimited dimensions:
    current shape = (412, 424)
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>

LON
    float32 lon(rlat, rlon)
        standard_name: longitude
        long_name: longitude coordinate
        units: degrees_east
        bounds: lon_vertices
    unlimited dimensions:
    current shape = (412, 424)
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>

LAT_VERTICES
    float32 lat_vertices(rlat, rlon, vertices)
        units: degrees_north
    unlimited dimensions:
    current shape = (412, 424, 4)
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>

LON_VERTICES
    float32 lon_vertices(rlat, rlon, vertices)
        units: degrees_east
    unlimited dimensions:
    current shape = (412, 424, 4)
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>

HEIGHT
    float64 height()
        units: m
        axis: Z
        positive: up
        long_name: height
        standard_name: height
    unlimited dimensions:
    current shape = ()
    filling on, default _FillValue of 9.969209968386869e+36 used, <class 'netCDF4._netCDF4.Variable'>

TAS
    float32 tas(time, rlat, rlon)
        standard_name: air_temperature
        long_name: Near-Surface Air Temperature
        comment: daily-mean near-surface (usually, 2 meter) air temperature.
        units: K
        cell_methods: time: mean
        coordinates: height lat lon
        missing_value: 1e+20
        _FillValue: 1e+20
        associated_files: gridspecFile: gridspec_atmos_fx_MPI-CSC-REMO2009_rcp45_r0i0p0.nc
        grid_mapping: rotated_latitude_longitude
    unlimited dimensions: time
    current shape = (60, 412, 424)
    filling on])