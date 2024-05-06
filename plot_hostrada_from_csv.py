import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataframe = pd.read_csv("out/hostrada_mai2023.csv", sep=";")

print(dataframe)


dataframe.plot(kind='line',
               x='time',
               y='temperature',
               color='pink',
               lw=1
               )
plt.title('Hostrada 2023, Loebauer 46')

# add lines at 20 degrees and at 30 degrees celsius
plt.axhline(20, color='blue', lw=0.5)
plt.axhline(30, color='red', lw=0.5)

# slice the year in quaters, for hour-based datasets for 1 year
# plt.axvline(2190, color='lightgray', lw=1)
# plt.axvline(4380, color='lightgray', lw=0.5)
# plt.axvline(6570, color='lightgray', lw=0.5)
plt.ylabel('Temperature [°C]')
plt.xlabel('Date and Time [mm-dd-hh]')
plt.minorticks_on()
# plt.grid(True)

plt.show()

# with open("out/test.txt", 'a') as outfile:
#    outfile.write("test")
#
#
# x = np.arange(0, 31, 1/24)
# y = np.arange(0, 31, 1/24)
#
# plot = plt.plot(x, y)
# fig = plt.figure()

# plt.show()
