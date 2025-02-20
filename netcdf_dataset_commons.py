import netCDF4


def get_index_of_closest_entry(entries, value):
    # Compute the squared distances (fast approximation)
    distances = (entries - value) ** 2
    # return index of min entry
    return distances.argmin()


class DerivedDataset:

    def __init__(self, path_to_file, main_variable):
        # PREPARE THE DATASET
        dataset = netCDF4.Dataset(path_to_file, 'r')

        # reading locations from the dataset
        self.lats = dataset.variables['lat'][:]
        self.lons = dataset.variables['lon'][:]

        self.dataset_times = dataset.variables['time'][:]
        self.dataset_variable = dataset.variables[main_variable][:]


    # a method to find the index of the grid point closest to the desired location
    def get_closest_gridpoints_indices(self, desired_lat, desired_lon):

        lat_index = get_index_of_closest_entry(self.lats, desired_lat)
        lon_index = get_index_of_closest_entry(self.lons, desired_lon)

        return lat_index, lon_index


    def get_coordinates_from_indices(self, location_coordinates):
        return self.lats[location_coordinates[0]], self.lons[location_coordinates[1]]


    # wrapper method to use for more than one location at once
    def find_closests_grid_points_indices(self, desired_locations):

        # collecting the indices on the grid closest to each desired location
        closest_grid_points_indices = []

        for location in desired_locations:
            grid_point_for_location = self.get_closest_gridpoints_indices(location[0], location[1])
            closest_grid_points_indices.append(grid_point_for_location)

        return closest_grid_points_indices

    # wrapper function to use for more than one tuple of indices at once
    def get_many_pretty_coordinates(self, index_tuple_list, decimal_places=1):
        pretty_coordinates = []
        for indexlat_indexlon in index_tuple_list:
            lat, lon = self.get_coordinates_from_indices(indexlat_indexlon)
            rounded_coordinates = lat.round(decimal_places), lon.round(decimal_places)
            pretty_coordinates.append(rounded_coordinates)
        return pretty_coordinates

    def get_pretty_times(self):
        return [1990, 1991, 1992]

    def get_pretty_data(self, location):
        return [800.4, 900.3, 200.2]
