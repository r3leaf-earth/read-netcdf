import sys

# infile_original_try = sys.argv[1]
path_to_try_files = '../../data/try/TRY_513564124162_Loebauer/'
try_files = ['TRY2045_513564124162_Jahr.dat', 'TRY2045_513564124162_Somm.dat', 'TRY2045_513564124162_Wint.dat']


# parse file for dates and temperatures only
def times_and_temperatures_from_file(infile_original_try):
    return select_columns_from_file(infile_original_try, 2, 6)


def temperatures_from_file(file):
    return select_columns_from_file(file,5, 6)


def select_columns_from_file(infile_original_try, first_column, last_column_exlusive):
    data = []
    with open(infile_original_try, 'r') as try_file:
        for line in try_file:

            # if line starts wiht letter or whitespace --> skip, because header
            if line and is_part_of_header(line):
                pass
            else:
                row = line.split()
                # only keep datetime and temperature
                data.append(row[first_column:last_column_exlusive])
    return data


def is_part_of_header(line):
    return line[0].isalpha() or line[0].isspace() or line[0] == "*"


data_year = times_and_temperatures_from_file(path_to_try_files + try_files[0])
data_summ = temperatures_from_file(path_to_try_files + try_files[1])
data_wint = temperatures_from_file(path_to_try_files + try_files[2])

lines = []
for i, row in enumerate(data_year):
    datetime = '-'.join(row[0:3])
    temperatures = ';'.join([row[3], data_summ[i][0], data_wint[i][0]])
    line = datetime + ';' + temperatures + '\n'
    lines.append(line)

with open("out/try.csv", 'a') as outfile:
    outfile.writelines(lines)

#      RW      HW MM DD HH     t    p  WR   WG N    x  RF    B    D   A    E IL
# ***
# 4162500 2733500  1  1  1   0.7 1006 245  0.5 7  3.5  85    0    0 291 -281  0
# 4162500 2733500  1  1  2   0.4 1006 242  0.6 7  3.4  85    0    0 287 -280  0
# 4162500 2733500  1  1  3   0.2 1005 239  0.6 7  3.3  85    0    0 282 -279  0
# 4162500 2733500  1  1  4   0.3 1004 240  0.6 7  3.3  84    0    0 280 -277  0
#
# [['1', '1', '1', '0.7'], ['1', '1', '2', '0.4'], ['1', '1', '3', '0.2'],
