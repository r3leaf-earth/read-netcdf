import sys

# infile_original_try = sys.argv[1]
path_to_try_files = '../../data/try/TRY_513564124162_Loebauer/'
try_files = ['TRY2045_513564124162_Jahr.dat', 'TRY2045_513564124162_Somm.dat', 'TRY2045_513564124162_Wint.dat']

column_headers = "RW      HW MM DD HH     t    p  WR   WG N    x  RF    B    D   A    E IL"
header_row = column_headers.split()

climate_variable_name = ''


# parse file for dates and temperatures only
def times_and_temperatures_from_file(infile_original_try):
    column_temperatures = 5
    set_climate_variable_name(column_temperatures)
    return select_columns_from_file(infile_original_try, 2, column_temperatures + 1)


def temperatures_from_file(file):
    column_temperatures = 5
    set_climate_variable_name(column_temperatures)
    return select_columns_from_file(file, column_temperatures, column_temperatures + 1)


def set_climate_variable_name(column_number_try_file):
    global climate_variable_name
    if header_row[column_number_try_file] == "t":
        climate_variable_name = "temperature"
    elif header_row[column_number_try_file] == "p":
        climate_variable_name = "air pressure"
    elif header_row[column_number_try_file] == "WR":
        climate_variable_name = "wind direction"
    elif header_row[column_number_try_file] == "WG":
        climate_variable_name = "wind speed"
    else:
        climate_variable_name = "which_climate_variable?"


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


# READ DATA INTO MEMORY (3 lists)
data_year = times_and_temperatures_from_file(path_to_try_files + try_files[0])
data_summ = temperatures_from_file(path_to_try_files + try_files[1])
data_wint = temperatures_from_file(path_to_try_files + try_files[2])

# PREPARE LINES FOR OUTFILE
climate_variables_header = ";".join([climate_variable_name + "_Jahr",
                                     climate_variable_name + "_Somm",
                                     climate_variable_name + "_Wint"])
outfile_column_headers = "time;" + climate_variables_header
data_lines = []
for i, row in enumerate(data_year):
    datetime = '-'.join(row[0:3])
    temperatures = ';'.join([row[3], data_summ[i][0], data_wint[i][0]])
    line = datetime + ';' + temperatures + '\n'
    data_lines.append(line)

# WRITE THE OUTFILE
with open("out/try.csv", 'a') as outfile:
    climate_variables = ";".join([climate_variable_name + "_Jahr", climate_variable_name + "_Somm", climate_variable_name + "_Wint"])
    outfile.write(outfile_column_headers + "\n")
    outfile.writelines(data_lines)

# EXAmPLE START OF A TRY-FILE
# Koordinatensystem : Lambert konform konisch
# Rechtswert        : 4162500 Meter
# Hochwert          : 2733500 Meter
# Hoehenlage        : 117 Meter ueber NN
# Erstellung des Datensatzes im Mai 2016
#
# Art des TRY       : extremer Sommer
# Bezugszeitraum    : 2031-2060
# Datenbasis 1      : Beobachtungsdaten Zeitraum 1995-2012
# Datenbasis 2      : Klimasimulationen Zeitraum 1971-2000 (Basis RCP-historical / CORDEX-Europa Laeufe)
# Datenbasis 3      : Klimasimulationen Zeitraum 2031-2060 (Basis RCP-4.5 und RCP-8.5 / CORDEX-Europa Laeufe)
#
# Format: (i7,1x,i7,1x,i2,1x,i2,1x,i2,1x,f5.1,1x,i4,1x,3i,1x,f4.1,1x,i1,1x,f4.1,1x,i3,1x,i4,1x,i4,1x,i3,1x,i4,2x,i1)
#
# Reihenfolge der Parameter:
# RW Rechtswert                                                    [m]       {3670500;3671500..4389500}
# HW Hochwert                                                      [m]       {2242500;2243500..3179500}
# MM Monat                                                                   {1..12}
# DD Tag                                                                     {1..28,30,31}
# HH Stunde (MEZ)                                                            {1..24}
# t  Lufttemperatur in 2m Hoehe ueber Grund                        [GradC]
# p  Luftdruck in Standorthoehe                                    [hPa]
# WR Windrichtung in 10 m Hoehe ueber Grund                        [Grad]    {0..360;999}
# WG Windgeschwindigkeit in 10 m Hoehe ueber Grund                 [m/s]
# N  Bedeckungsgrad                                                [Achtel]  {0..8;9}
# x  Wasserdampfgehalt, Mischungsverhaeltnis                       [g/kg]
# RF Relative Feuchte in 2 m Hoehe ueber Grund                     [Prozent] {1..100}
# B  Direkte Sonnenbestrahlungsstaerke (horiz. Ebene)              [W/m^2]   abwaerts gerichtet: positiv
# D  Diffuse Sonnenbetrahlungsstaerke (horiz. Ebene)               [W/m^2]   abwaerts gerichtet: positiv
# A  Bestrahlungsstaerke d. atm. Waermestrahlung (horiz. Ebene)    [W/m^2]   abwaerts gerichtet: positiv
# E  Bestrahlungsstaerke d. terr. Waermestrahlung                  [W/m^2]   aufwaerts gerichtet: negativ
# IL Qualitaetsbit bezueglich der Auswahlkriterien                           {0;1;2;3;4}
#
#
#      RW      HW MM DD HH     t    p  WR   WG N    x  RF    B    D   A    E IL
# ***
# 4162500 2733500  1  1  1  -0.2 1006 201  0.8 5  3.2  84    0    0 291 -281  2
# 4162500 2733500  1  1  2  -0.1 1006 220  0.7 6  3.3  85    0    0 287 -280  2
# 4162500 2733500  1  1  3   0.2 1005 239  0.6 7  3.3  85    0    0 282 -279  2
# 4162500 2733500  1  1  4   0.3 1004 240  0.6 7  3.3  84    0    0 280 -277  2
# 4162500 2733500  1  1  5   0.5 1004 238  0.7 7  3.3  83    0    0 279 -279  2
# 4162500 2733500  1  1  6   0.9 1003 250  0.8 7  3.3  82    0    0 280 -284  2
# 4162500 2733500  1  1  7   1.0 1003 231  1.6 7  3.3  81    0    0 282 -288  2
