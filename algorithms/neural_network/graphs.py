import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

mean = pd.read_csv('Val-Results-Belgium/2021-May-15/10-30/pred_all.csv')
meanval = mean['Infected']
dates = mean['Data']
first_date = mean.query('`Used in Train` == False')['Data'].reset_index(drop=True).get(0)
max = pd.read_csv('Val-Results-Belgium/2021-May-15/10-30/pred_all_max.csv')['Infected']
min = pd.read_csv('Val-Results-Belgium/2021-May-15/10-30/pred_all_min.csv')['Infected']

fig, ax = plt.subplots()
ax.plot(dates, meanval, color='black')
ax.plot(dates, max, '-.', color='red')
ax.plot(dates, min, '-.', color='red')
ax.fill_between(dates, min, max, color='lightsteelblue')

ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))

plt.axvline(first_date, color='black', ls=':')

plt.show()