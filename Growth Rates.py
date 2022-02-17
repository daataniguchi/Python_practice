import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def mean_data_chl_1(file, sheet, group, cols): #creates chl_1 values
    data = pd.read_excel(file , sheet_name=sheet, usecols= cols) #reads data
    drop = data.drop([0,1,2]).replace(0, np.nan).dropna(axis=1, how='all') #drops chl_0 rows and replaces any 0 values with NA then drops them
    df = drop.loc[drop['Time_point'] == 1].groupby(group, as_index=False, dropna=True, sort=False).mean() #selects only rows with time point = 1, groups by bottle number and takes the average
    return df

def mean_data_chl_2(file, sheet, group, cols): #creates chl_2 values
    data = pd.read_excel(file , sheet_name=sheet, usecols= cols) #reads data
    drop = data.drop([0,1,2]).replace(0, np.nan).dropna(axis=1, how='all') #drops chl_0 rows and replaces any 0 values with NA then drops them
    df = drop.loc[drop['Time_point'] == 2].groupby(group, as_index=False, dropna=True, sort=False).mean() #selects only rows with time point = 2, groups by bottle number and takes the average
    return df

def chl_0(file, sheet, cols): #chl value used as chl_0
    data = pd.read_excel(file, sheet_name=sheet, usecols= cols) #reads data
    data['Chlorophyll, ug/L'] = data['Chlorophyll, ug/L'].replace(0, np.nan) #replaces any chl = 0 values with NA
    value = data.loc[data['Time_point'] == 0].mean() #selects only rows with time point 0 and takes the average
    chl_0 = value['Chlorophyll, ug/L'] #locates chl_0 value
    return chl_0

def graph_rates(x,y): #create rates scatter plot
    m, b = np.polyfit(x, y , 1) #creates variable for line of best fit
    plt.scatter(x, y) #plots x, y values
    plt.plot(x, m*x+b) #plots line of best fit
    plt.xlabel('Fraction whole seawater')
    plt.ylabel('Apparent growth rate day')
    print('Growth rate =' , b) #prints y-int aka growth rate
    print('Grazing rate =' , -m) #prints slope aka grazing rate
    plt.show()

x = chl_0('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx', 'Experiment_4', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater']) #grabbing chl0 value
avg_data_chl_1 = mean_data_chl_1('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx','Experiment_4', 'Bottle_number', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'])
avg_data_chl_2 = mean_data_chl_2('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx','Experiment_4', 'Bottle_number', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'])


avg_data_chl_1['Apparent growth rate day'] = 2*np.log((avg_data_chl_1['Chlorophyll, ug/L']/(x*avg_data_chl_1['Fraction_whole_seawater']))) #calculating day growth rates
avg_data_chl_1['Apparent growth rate night'] = 2*np.log(avg_data_chl_2['Chlorophyll, ug/L']/avg_data_chl_1['Chlorophyll, ug/L']) #calculates night growing rates
avg_data_chl_1['Apparent growth rate 24 hrs'] = 1*np.log((avg_data_chl_2['Chlorophyll, ug/L']/(x*avg_data_chl_2['Fraction_whole_seawater']))) #calculating 24 hrs growth rates


graph_rates(avg_data_chl_1['Fraction_whole_seawater'], avg_data_chl_1['Apparent growth rate day'])






