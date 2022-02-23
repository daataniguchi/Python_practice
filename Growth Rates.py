import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def mean_data(file, sheet, group, cols): #creates dataframe to work with
    data = pd.read_excel(file , sheet_name=sheet, usecols= cols) #read data
    drop = data.drop([0,1,2]).replace(0, np.nan).dropna(axis=1, how='all') #drops first 3 columns, converts any 0 into NaN and drops them
    df = drop.groupby(group, as_index=False, dropna=True, sort=False).mean() #groups by variable and averages it
    return df

def chl_0(file, sheet, cols): #chl value used as chl0
    data = pd.read_excel(file, sheet_name=sheet, usecols= cols) #reads data
    data['Chlorophyll, ug/L'] = data['Chlorophyll, ug/L'].replace(0, np.nan) #specified chlorophyll column and raplaces any 0 with NaN
    value = data.loc[data['Time_point'] == 0].mean() #identifies rows with timepoint = 0 and averages them
    chl_0 = value['Chlorophyll, ug/L'] #creates chl_0 variable
    return chl_0

def graph_rates(x, y): #create rates scatter plot
    m, b = np.polyfit(x, y , 1) #creates variable for line of best fit
    plt.scatter(x, y) #plots x, y values
    plt.plot(x, m*x+b) #plots line of best fit
    plt.errorbar(x, y, yerr=error, fmt='o', ecolor= 'blue', color= 'blue') #creates error bar
    plt.xlabel('Fraction whole seawater')
    plt.ylabel('Apparent growth rate day')
    print('Growth rate =' , b) #prints y-int aka growth rate
    print('Grazing rate =' , -m) #prints slope aka grazing rate
    plt.show()

file = 'C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx' #selects file
experiment = 'Experiment_6' #select experiment to work on
data = mean_data(file, experiment , 'Bottle_number', ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater']) #grabbing dataframe
chl_0 = chl_0('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx', experiment , ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater']) #grabbing chl0 value
chl_1 = data.loc[data['Time_point'] == 1] #selects data with timepoint = 1
chl_2 = data.loc[data['Time_point'] == 2].reset_index(drop=True) #selects data with timepoint = 2 and resets index

data['Apparent growth rate day'] = 2*np.log((chl_1['Chlorophyll, ug/L']/(chl_0*chl_1['Fraction_whole_seawater']))) #calculating day apparent growth rates
data['Apparent growth rate night'] = 2*np.log(chl_2['Chlorophyll, ug/L']/chl_1['Chlorophyll, ug/L']) #calculating night apparent growth rates
data['Apparent growth rate 24 hrs'] = 1*np.log((chl_2['Chlorophyll, ug/L']/(chl_0*chl_2['Fraction_whole_seawater']))) #calculating 24 hr apparent growth rates
final_data = data.dropna() #drops any NaN in the dataframe

time_rate = final_data['Apparent growth rate day'] #selects apparent growth rate to work on
error = np.std(time_rate)/np.sqrt(len(time_rate)) #calculates standard error used for error bars

graph_rates(final_data['Fraction_whole_seawater'], time_rate) #creates graph


