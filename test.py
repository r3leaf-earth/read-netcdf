import unittest

import numpy as np

def get_index_of_min(distances):
        return distances.argmin()
        # min_index = np.unravel_index(np.argmin(distances), distances.shape)
        # return min_index


def get_closest_gridpoints_indices(lats, lons, desired_lat, desired_lon):

    # Compute the squared differences (fast approximation)
    lat_diffs = (lats - desired_lat) ** 2
    lon_diffs = (lons - desired_lon) ** 2

    print(lat_diffs)

    # min and index of
    lat_index = get_index_of_min(lat_diffs)
    lon_index = get_index_of_min(lon_diffs)

    print(lat_diffs.argmin(), lon_diffs.argmin())

    return lat_index, lon_index


class MyTestCase(unittest.TestCase):
    def test_something(self):
        lats = np.array([50.5, 50.75, 51., 51.25, 51.5, 51.75, 52., 52.25,
                52.5, 52.75, 53., 53.25, 53.5, 53.75, 54., 54.25,
                54.5, 54.75, 55., 55.25, 55.5, 55.75, 56., 56.25,
                56.5, 56.75, 57., 57.25, 57.5, 57.75, 58., 58.25,
                58.5, 58.75, 59., 59.25, 59.5, 59.75, 60., 60.25,
                60.5, 60.75, 61., 61.25, 61.5, 61.75, 62., 62.25,
                62.5, 62.75, 63., 63.25, 63.5, 63.75, 64., 64.25,
                64.5, 64.75, 65., 65.25, 65.5, 65.75, 66., 66.25,
                66.5, 66.75, 67., 67.25, 67.5, 67.75, 68., 68.25,
                68.5, 68.75, 69., 69.25, 69.5, 69.75, 70., 70.25,
                70.5, 70.75, 71., 71.25, 71.5, 71.75, 72., 72.25,
                72.5])

        lons = np.array([9.5, 9.75, 10., 10.25, 10.5, 10.75, 11.,
                11.25, 11.5, 11.75, 12., 12.25, 12.5, 12.75,
                13., 13.25, 13.5, 13.75, 14., 14.25, 14.5,
                14.75, 15., 15.25, 15.5, 15.75, 16., 16.25,
                16.5, 16.75, 17., 17.25, 17.5, 17.75, 18.,
                18.25, 18.5, 18.75, 19., 19.25, 19.5, 19.75,
                20., 20.25, 20.5, 20.75, 21., 21.25, 21.5,
                21.75, 22., 22.25, 22.5, 22.75, 23., 23.25,
                23.5, 23.75, 24., 24.25, 24.5, 24.75, 25.,
                25.25, 25.5, 25.75, 26., 26.25, 26.5, 26.75,
                27., 27.25, 27.5, 27.75, 28., 28.25, 28.5,
                28.75, 29., 29.25, 29.5, 29.75, 30., 30.25,
                30.5, 30.75, 31., 31.25, 31.5, 31.75, 32.,
                32.25, 32.5, 32.75, 33., 33.25, 33.5, 33.75,
                34., 34.25, 34.5, 34.75, 35., 35.25, 35.5,
                35.75, 36., 36.25, 36.5, 36.75, 37., 37.25,
                37.5, 37.75, 38., 38.25, 38.5, 38.75, 39.,
                39.25, 39.5, 39.75, 40., 40.25, 40.5, 40.75,
                41., 41.25, 41.5, 41.75, 42., 42.25, 42.5,
                42.75, 43., 43.25, 43.5, 43.75, 44., 44.25,
                44.5, 44.75, 45., 45.25, 45.5])


        grid_lat_index, grid_lon_index = get_closest_gridpoints_indices(lats, lons, 55.1, 38.70)

        closest_lat = lats[grid_lat_index]
        closest_lon = lons[grid_lon_index]

        print(lats[18], lons[117])

        self.assertEqual(closest_lat, 55.0)  # add assertion here
        self.assertEqual(closest_lon, 38.75)  # add assertion here


if __name__ == '__main__':
    unittest.main()
