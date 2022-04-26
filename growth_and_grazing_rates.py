import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import seaborn as sns
def orig_data(file, sheet, group, cols):
    data = pd.read_excel(file, sheet_name=sheet)
    drop = data.drop([0,1,2]).replace(0, np.nan).dropna(axis=1, how='all')
    df = drop[cols].groupby(group, as_index=False, dropna=True, sort=False).mean()
    return df

def chlorophyll_tp_0(file, sheet, cols): #chl value used as chl0
    data = pd.read_excel(file, sheet_name=sheet, usecols= cols) #reads data
    data['Chlorophyll, ug/L'] = data['Chlorophyll, ug/L'].replace(0, np.nan) #specified chlorophyll column and raplaces any 0 with NaN
    value = data.loc[data['Time_point'] == 0].mean() #identifies rows with timepoint = 0 and averages them
    chl_0 = value['Chlorophyll, ug/L'] #creates chl_0 variable
    return chl_0

def chl_data(file, sheet, group, cols, timepoint): #creates dataframe to work with
    data = pd.read_excel(file , sheet_name=sheet, usecols= cols) #read data
    drop = data.dropna(axis=1, how='all') #drops first 3 columns, converts any 0 into NaN and drops them
    df = drop.loc[drop['Time_point'] == timepoint].groupby(group, as_index=False, dropna=True, sort=False).mean() #groups by variable and averages it
    return df

def graph_rates(x, y): #create rates scatter plot
    m, b = np.polyfit(x, y , 1) #creates variable for line of best fit
    plt.scatter(x, y) #plots x, y values
    plt.plot(x, m*x+b) #plots line of best fit
    plt.errorbar(x, y, yerr=error, fmt='o', ecolor='blue', color='blue')
    plt.xlabel('Fraction whole seawater')
    plt.ylabel('Apparent growth rate day')
    print('Growth rate =' , b) #prints y-int aka growth rate
    print('Grazing rate =' , -m) #prints slope aka grazing rate
    plt.show()

def graph_values(data):
    df = pd.DataFrame.from_dict({(i, j): data[i][j] for i in data.keys() for j in data[i].keys()}, orient='index').reset_index().rename(columns={'level_0': 'Location', 'level_1': 'Experiment'}).melt(['Location', 'Start_time', 'Experiment']).rename(columns={'variable': 'Rate'})
    sns.scatterplot(x='Location', y='value', data=df, marker='.', style='Start_time', hue='Rate', sort= False)


file = 'C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx'
f = pd.ExcelFile('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx')
experiment = f.sheet_names #select experiment to work on


growth = {}
grazing = {}
net = {}
r2_value = {}
e_even = []
e_odd = []
for e in experiment:
    if e == 'Profiles':
        continue
    data = orig_data(file, e, ['Station_description', 'Bottle_number'], ['Sampling_start_time', 'Station_description', 'Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'])
    chl_0 = chlorophyll_tp_0(file, e, ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'])  # selects data with timepoint = 2 and resets index
    chl_1 = chl_data(file, e, 'Bottle_number', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'], 1)
    chl_2 = chl_data(file, e, 'Bottle_number', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'], 2)
    data['Day_rate'] = 2 * np.log((chl_1['Chlorophyll, ug/L'] / (chl_0 * chl_1['Fraction_whole_seawater'])))  # calculating day apparent growth rates
    data['Night_rate'] = 2 * np.log(chl_2['Chlorophyll, ug/L'] / chl_1['Chlorophyll, ug/L'])  # calculating night apparent growth rates
    data['24_hrs_rate'] = 1 * np.log((chl_2['Chlorophyll, ug/L'] / (chl_0 * chl_2['Fraction_whole_seawater'])))  # calculating 24 hr apparent growth rates
    final_data = data.dropna()
    if final_data['Sampling_start_time'].iloc[0] > 1000:
        e_even.append(e)
    else:
        e_odd.append(e)
    time_rate = ['Day_rate', 'Night_rate', '24_hrs_rate']
    station = data['Station_description'].iloc[0]
    if station not in growth and station not in grazing:
        growth[station] = {}
        grazing[station] = {}
        net[station] = {}
        r2_value[station] = {}
    else:
        growth[station].update()
        growth[station].update()
        net[station].update()
        r2_value[station].update()
    if e in growth and e in grazing:
        growth[station][e].update()
        grazing[station][e].update()
        net[station][e].update()
        growth_r2_value[station][e].update()
    elif e not in growth and e not in grazing:
        growth[station][e] = {}
        grazing[station][e] = {}
        net[station][e]= {}
        r2_value[station][e] = {}
    if e in e_even:
        growth[station][e].update({'Start_time':'Daytime'})
        grazing[station][e].update({'Start_time': 'Daytime'})
        net[station][e].update({'Start_time': 'Daytime'})
    elif e in e_odd:
        growth[station][e].update({'Start_time':'Nighttime'})
        grazing[station][e].update({'Start_time': 'Nighttime'})
        net[station][e].update({'Start_time': 'Nighttime'})
    for t in time_rate:
        m, b = np.polyfit(final_data['Fraction_whole_seawater'], final_data[t], 1)
        growth[station][e][t]= b
        grazing[station][e][t]= -m
        net[station][e][t] = b - (-m)
        corr_matrix = np.corrcoef(final_data['Fraction_whole_seawater'], final_data[t])
        corr = corr_matrix[0, 1]
        R_sq = corr ** 2
        r2_value[station][e][t] = R_sq

df = pd.DataFrame.from_dict({(i, j): growth[i][j] for i in growth.keys() for j in growth[i].keys()}, orient='index').reset_index().rename(columns={'level_0': 'Location', 'level_1': 'Experiment'}).melt(['Location', 'Start_time', 'Experiment']).rename(columns={'variable': 'Rate'})


print('grazing rates:', grazing)
print('growth rates:', growth)
print('net rates:', net)
print('r2 values are:', r2_value)


fig1 = graph_values(growth)
plt.show()
fig2 = graph_values(grazing)
plt.show()

