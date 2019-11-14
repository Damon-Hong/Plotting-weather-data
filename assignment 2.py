import pandas as pd
df = pd.read_csv('fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df = df.drop('ID', axis = 1)
df_index = pd.DatetimeIndex(df['Date'])
df = df[~ ((df_index.is_leap_year) & (df_index.month == 2) & (df_index.day == 29))]
df_index = pd.DatetimeIndex(df['Date'])
df['Month'] = df_index.month
df['Day'] = df_index.day
df_2005 = df[df_index < '2005-01-01'] # therefore, all the datetime are larger than 2005-01-01
df_2015 = df[df_index >= '2015-01-01']
df = df[df_index <= '2015-01-01'] # our new df
df_max = df[df['Element'] == 'TMAX'].groupby(['Month','Day'])['Data_Value'].max()
df_max = df_max/10
df_min = df[df['Element'] == 'TMIN'].groupby(['Month', 'Day'])['Data_Value'].min()
df_min = df_min/10
df_2015_max = df_2015[df_2015['Element'] == 'TMAX'].groupby(['Month', 'Day'])['Data_Value'].max()
df_2015_max = df_2015_max/10
df_2015_min = df_2015[df_2015['Element'] == 'TMIN'].groupby(['Month', 'Day'])['Data_Value'].min()
df_2015_min = df_2015_min/10
import numpy as np
x_axis = np.arange('2015-01-01', '2016-01-01', dtype = 'datetime64[D]')
x_axis = np.array(list(map(pd.to_datetime, x_axis)))
max_broken = (df_2015_max > df_max).values
min_broken = (df_2015_min< df_min).values
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.figure()
plt.plot(x_axis, df_max, '-', color = 'blue')
plt.plot(x_axis, df_min, '-', color = 'green')
plt.plot(x_axis[max_broken], df_2015_max[max_broken], 'r^', color = 'red')
plt.plot(x_axis[min_broken], df_2015_min[min_broken], 'bv', color = 'red')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().fill_between(x_axis, df_min, df_max, facecolor='pink', alpha=0.45)
plt.legend(['max in 2005-2014', 'min in 2005-2014', 'max broken point', 'min broken point'])
plt.xlabel('Months in a year')
plt.ylabel('temperature')
plt.title('max and min temperature in 2005-2014 & 2015 broken point')
plt.show()