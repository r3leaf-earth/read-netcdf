import matplotlib.pyplot as plt
import pandas as pd

dataframe = pd.read_csv("out/hostrada.csv", sep=";")

print(dataframe)

dataframe.plot(kind='line',
               x='time',
               y='tas',
               color='turquoise',
               lw=1
               )
plt.title('Hostr-UHI 2023, Loebauer 46')

# add lines at 20 degrees and at 30 degrees celsius (useful for climate variable tas)
# plt.axhline(20, color='blue', lw=0.5)
# plt.axhline(30, color='red', lw=0.5)
plt.axhline(3, color='gray', lw=0.5)

# slice the year in quaters, for hour-based datasets for 1 year
# plt.axvline(2190, color='lightgray', lw=1)
# plt.axvline(4380, color='lightgray', lw=0.5)
# plt.axvline(6570, color='lightgray', lw=0.5)
# plt.ylabel('Temperature [°C]')
plt.xlabel('Date and Time [YYYY-MM-DD hh:mm:ss]')
plt.minorticks_on()
# plt.grid(True)

plt.show()
