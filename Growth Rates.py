import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def mean_data(file, sheet, group, cols):
    data = pd.read_excel(file , sheet_name=sheet, usecols= cols)
    drop_0 = data.drop([0,1,2])
    print(drop_0)
    drop = drop_0.drop(drop_0.index[42:84])
    print(drop)
    df = drop.groupby(group, as_index=False, dropna=True).mean()
    return df

def chl_0(file, sheet): #chl value used as chl0
    data = pd.read_excel(file, sheet_name=sheet)
    value = data['Chlorophyll, ug/L'].values[0]
    return value


x = chl_0('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx', 'Experiment_4') #grabbing chl0 value

avg_data = mean_data('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx','Experiment_4', 'Bottle_number', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'])
print(avg_data)
avg_data['Apparent growth rate day'] = 2*np.log((avg_data['Chlorophyll, ug/L']/(x*avg_data['Fraction_whole_seawater']))) #calculating day growth rates



plt.scatter(avg_data['Fraction_whole_seawater'], avg_data['Apparent growth rate day'], ) #plotting growth rates
plt.show()



