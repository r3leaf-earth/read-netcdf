# read-cordex-netcdf
The script 'read_tas.py' reads variables from a netCDF file which belongs to climate models CORDEX.

The variable read is the daily mean temperature 2m above the ground level, short 'tas'.

## For whom?
If you are starting to work with .nc-files this is a good starting point for you.

### Am I Looking at the Right Data?
Climate Projection Data is a large field. If you are an end user, like me, you might want to keep searching for already processed datasets. For example: From climate projection data one can analyse heat days and heat waves, because they contain a maximum daily temperature. Someone has already done this analysis.


## How to Run the Script
Run information is located at the beginning of the script itself. Check "Prerequisites" and "Usage". 

## What's up with that File 'variables_values.md'?
It contains some information about the structure of the data in the .nc file. 
You can reproduce the outputs (or get different ones) with the steps below.

Since CORDEX-data have a standardized structure, you might get the same responses from your .nc-file.

It depends on the query.

### Take a look into the Datastructure via the Python-shell
1. Pip install netCDF as mentioned in the script.

2. Start the python interpreter from your terminal
```sh
python
```

3. Import netCDF and your file. Replace 'path_to_file_and_name.nc' with your filename and location
```python
>>> import netCDF
>>> dataset = netCDF.Dataset('path_to_file_and_name.nc')
```

4. Then, try the commands from 'variables_values.md'
```python
>>> dataset.dimensions.keys()
>>> dataset.variables.keys()
>>> dataset.variables['tas'] # if 'tas' was part of the variables.keys() above
```

## Contributing
We appreciate your contributions! In fact, we decided to open-source this simple script mainly to connect with others working on similar topics. Leave us a note in Discussions!

### How to Contribute to the Code
Just open a PR or an Issue.
Make sure to give some context, WHY this change is useful and HOW your need for the change came to be.
Thank you!!
