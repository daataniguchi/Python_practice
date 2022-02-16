import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def mean_data_chl_1(file, sheet, group, cols):
    data = pd.read_excel(file , sheet_name=sheet, usecols= cols)
    drop = data.drop([0,1,2]).replace(0, np.nan).dropna(axis=1, how='all')
    df = drop.loc[drop['Time_point'] == 1].groupby(group, as_index=False, dropna=True, sort=False).mean()
    return df

def mean_data_chl_2(file, sheet, group, cols):
    data = pd.read_excel(file , sheet_name=sheet, usecols= cols)
    drop = data.drop([0,1,2]).replace(0, np.nan).dropna(axis=1, how='all')
    df = drop.loc[drop['Time_point'] == 2].groupby(group, as_index=False, dropna=True, sort=False).mean()
    return df

def chl_0(file, sheet, cols): #chl value used as chl0
    data = pd.read_excel(file, sheet_name=sheet, usecols= cols)
    data['Chlorophyll, ug/L'] = data['Chlorophyll, ug/L'].replace(0, np.nan)
    value = data.loc[data['Time_point'] == 0].mean()
    chl_0 = value['Chlorophyll, ug/L']
    return chl_0


x = chl_0('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx', 'Experiment_4', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater']) #grabbing chl0 value
print(x)
avg_data_chl_1 = mean_data_chl_1('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx','Experiment_4', 'Bottle_number', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'])
print(avg_data_chl_1)
avg_data_chl_2 = mean_data_chl_2('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx','Experiment_4', 'Bottle_number', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'])
print(avg_data_chl_2)


avg_data_chl_1['Apparent growth rate day'] = 2*np.log((avg_data_chl_1['Chlorophyll, ug/L']/(x*avg_data_chl_1['Fraction_whole_seawater']))) #calculating day growth rates
avg_data_chl_1['Apparent growth rate night'] = 2*np.log(avg_data_chl_2['Chlorophyll, ug/L']/avg_data_chl_1['Chlorophyll, ug/L'])
avg_data_chl_1['Apparent growth rate 24 hrs'] = 1*np.log((avg_data_chl_2['Chlorophyll, ug/L']/(x*avg_data_chl_2['Fraction_whole_seawater'])))
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(avg_data_chl_1)




