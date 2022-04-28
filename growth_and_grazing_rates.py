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

def chl_data(file, sheet, group, cols, timepoint): #creates dataframe to work with
    data = pd.read_excel(file , sheet_name=sheet, usecols= cols) #read data
    drop = data.dropna(axis=1, how='all') #drops first 3 columns, converts any 0 into NaN and drops them
    df = drop.loc[drop['Time_point'] == timepoint].groupby(group, as_index=False, dropna=True, sort=False).mean() #groups by variable and averages it
    return df

def graph_apparent_rates(x, y): #create rates scatter plot
    m, b = np.polyfit(x, y , 1) #creates variable for line of best fit
    plt.scatter(x, y) #plots x, y values
    plt.plot(x, m*x+b) #plots line of best fit
    plt.errorbar(x, y, yerr=error, fmt='o', ecolor='blue', color='blue')
    plt.xlabel('Fraction whole seawater')
    plt.ylabel('Apparent growth rate day')
    print('Growth rate =' , b) #prints y-int aka growth rate
    print('Grazing rate =' , -m) #prints slope aka grazing rate
    plt.show()

def graph_actual_rates(data):
    df = pd.DataFrame.from_dict({(i, j): data[i][j] for i in data.keys() for j in data[i].keys()}, orient='index').reset_index().rename(columns={'level_0': 'Location', 'level_1': 'Experiment'}).melt(['Location', 'Start_time', 'Experiment']).rename(columns={'variable': 'Rate'})
    df['Location'] = pd.Categorical(df['Location'], categories=['Offshore', 'Shelf_break', 'Mid_shelf', 'Nearshore'], ordered=True)
    plt.figure(figsize=(11, 8))
    sns.set_style('dark')
    sns.set_context('talk')
    sns.scatterplot(x='Location', y='value', data=df, style='Rate', size='Start_time', hue='Rate')
    if data == growth:
        plt.ylabel('Growth Rate (1/Day)')
        plt.ylim((-0.30, 1.90))
    elif data == grazing:
        plt.ylabel('Grazing Mortality Rate (1/Day')
        plt.ylim((-0.30, 1.90))
    elif data == net:
        plt.ylabel('Net Growth Rate (1/Day)')
    plt.show()


file = 'C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx'
f = pd.ExcelFile('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx')
experiment = f.sheet_names #select experiment to work on


growth = {}
grazing = {}
net = {}
r2_value = {}
e_even = []
e_odd = []
st_error = []
for e in experiment:
    if e == 'Profiles':
        continue
    data = orig_data(file, e, ['Station_description', 'Bottle_number'], ['Sampling_start_time', 'Station_description', 'Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'])
    chl_0 = chl_data(file, e, ['Bottle_number', 'Time_point'], ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'], 0)
    chl_1 = chl_data(file, e, ['Bottle_number', 'Time_point'], ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'], 1)
    chl_2 = chl_data(file, e, ['Bottle_number', 'Time_point'], ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'], 2)
    data['Day_rate'] = 2 * np.log((chl_1['Chlorophyll, ug/L'] / (chl_0['Chlorophyll, ug/L'].values[0] * chl_1['Fraction_whole_seawater'])))  # calculating day apparent growth rates
    data['Night_rate'] = 2 * np.log(chl_2['Chlorophyll, ug/L'] / chl_1['Chlorophyll, ug/L'])  # calculating night apparent growth rates
    data['24_hrs_rate'] = 1 * np.log((chl_2['Chlorophyll, ug/L'] / (chl_0['Chlorophyll, ug/L'].values[0] * chl_2['Fraction_whole_seawater']))) # calculating 24 hr apparent growth rates
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
        error = np.std(final_data[t]) / np.sqrt(len(final_data[t]))
        st_error.append(error)
        growth[station][e][t]= b
        grazing[station][e][t]= -m
        net[station][e][t] = b - (-m)
        corr_matrix = np.corrcoef(final_data['Fraction_whole_seawater'], final_data[t])
        corr = corr_matrix[0, 1]
        R_sq = corr ** 2
        r2_value[station][e][t] = R_sq

graph_actual_rates(growth)
graph_actual_rates(grazing)
graph_actual_rates(net)
"""
print('grazing rates:', grazing)
print('growth rates:', growth)
print('net rates:', net)
print('r2 values are:', r2_value)
"""

