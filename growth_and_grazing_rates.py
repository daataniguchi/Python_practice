import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import seaborn as sns
def orig_data(file, sheet, group, cols): #grabs data to manipulate
    data = pd.read_excel(file, sheet_name=sheet) #loads in excel file
    drop = data.drop([0,1,2]).replace(0, np.nan).dropna(axis=1, how='all') #Drops the first 3 rows, replaces any 0 values with NaN, and drops all NaN values
    df = drop[cols].groupby(group, as_index=False, dropna=True, sort=False).mean() #Selects which columns to use, groups by column values and takes the average values
    return df

def chl_data(file, sheet, group, cols, timepoint): #creates dataframe to work with
    data = pd.read_excel(file , sheet_name=sheet, usecols= cols) #read data
    drop = data.dropna(axis=1, how='all') #drops first 3 columns, converts any 0 into NaN and drops them
    df = drop.loc[drop['Time_point'] == timepoint].groupby(group, as_index=False, dropna=True, sort=False).mean() #selects time_point to use, groups by variable and averages it
    return df

def graph_apparent_rates(x, y): #create rates scatter plot
    m, b = np.polyfit(x, y , 1) #creates variable for line of best fit
    plt.scatter(x, y) #plots x, y values
    plt.plot(x, m*x+b) #plots line of best fit
    plt.errorbar(x, y, yerr=error, fmt='o', ecolor='blue', color='blue') #vizualizes error bar
    plt.xlabel('Fraction whole seawater') #creates x label
    plt.ylabel('Apparent growth rate day') #creates y label
    print('Growth rate =' , b) #prints y-int aka growth rate
    print('Grazing rate =' , -m) #prints slope aka grazing rate
    plt.show()

def graph_actual_rates(data): #graphs rates
    #vvvv converts nested dictionary into dataframe, resets index so index is not categories, renames columns, combines rate columns into one for easier plotting, renames variable column to Rate vvvv
    df = pd.DataFrame.from_dict({(i, j): data[i][j] for i in data.keys() for j in data[i].keys()}, orient='index').reset_index().rename(columns={'level_0': 'Location', 'level_1': 'Experiment'}).melt(['Location', 'Start_time', 'Experiment']).rename(columns={'variable': 'Rate'})
    df['Location'] = pd.Categorical(df['Location'], categories=['Offshore', 'Shelf_break', 'Mid_shelf', 'Nearshore'], ordered=True) #changes catergorical axis order into desired order
    plt.figure(figsize=(11, 8)) #sets figure size
    sns.set_style('dark') #sets figure style
    sns.set_context('talk') #secondary figure style
    sns.scatterplot(x='Location', y='value', data=df, style='Rate', size='Start_time', hue='Rate') #creates scatterplot, style changes marker shape, size changes marker size, and hue changes marker color
    if data == growth: #if parameter is growth
        plt.ylabel('Growth Rate (1/Day)') #changes y axis title
        plt.ylim((-0.35, 1.90)) #changes y axix limits
    elif data == grazing: #if parameter is grazing
        plt.ylabel('Grazing Mortality Rate (1/Day') #changes y axis title
        plt.ylim((-0.35, 1.90)) #changes y axis limits
    elif data == net: #if paramer is net
        plt.ylabel('Net Growth Rate (1/Day)') #changes y axis title
    plt.show() #shows figure


file = 'C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx' #excel file to be used
f = pd.ExcelFile(file) #changes file so we can read the sheet names
experiment = f.sheet_names #creates list of sheet names


growth = {} #creates growth dictionary
grazing = {} #creates grazing dictionary
net = {} #creates net dictionary
r2_value = {} #creates r2 values dictionary
day_start = [] #creates day start list of experiments
night_start = [] #creates night start list of experiments
st_error = [] #creates standard error list
for e in experiment: #for every item in the experiment list
    if e == 'Profiles': #if item is equal to Profiles sheet
        continue #do nothing
    data = orig_data(file, e, ['Station_description', 'Bottle_number'], ['Sampling_start_time', 'Station_description', 'Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater']) #create primary dataframe
    chl_0 = chl_data(file, e, ['Bottle_number', 'Time_point'], ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'], 0) #create dataframe for time points 0
    chl_1 = chl_data(file, e, ['Bottle_number', 'Time_point'], ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'], 1) #create dataframe for timepoints 1
    chl_2 = chl_data(file, e, ['Bottle_number', 'Time_point'], ['Chlorophyll, ug/L', 'Bottle_number', 'Time_point', 'Fraction_whole_seawater'], 2) #create dataframe for timepoints 2
    data['Day_rate'] = 2 * np.log((chl_1['Chlorophyll, ug/L'] / (chl_0['Chlorophyll, ug/L'].values[0] * chl_1['Fraction_whole_seawater'])))  # calculating day apparent growth rates
    data['Night_rate'] = 2 * np.log(chl_2['Chlorophyll, ug/L'] / chl_1['Chlorophyll, ug/L'])  # calculating night apparent growth rates
    data['24_hrs_rate'] = 1 * np.log((chl_2['Chlorophyll, ug/L'] / (chl_0['Chlorophyll, ug/L'].values[0] * chl_2['Fraction_whole_seawater']))) # calculating 24 hr apparent growth rates
    final_data = data.dropna() #drop any NaN values in the dataframe
    if final_data['Sampling_start_time'].iloc[0] > 1000:
        day_start.append(e) #if start time is higher than 1000 add experiment to day_start list
    else:
        night_start.append(e) #if start time is lower than 1000 add experiment to night start list
    time_rate = ['Day_rate', 'Night_rate', '24_hrs_rate'] #set time rates
    station = data['Station_description'].iloc[0] #locate location of the experiment
    if station not in growth and station not in grazing: #if station is not a key in the dictionaries, create it and add experiment as value
        growth[station] = {}
        grazing[station] = {}
        net[station] = {}
        r2_value[station] = {}
    else:
        growth[station].update() #if station is a key in the dictionaries, add value to key
        growth[station].update()
        net[station].update()
        r2_value[station].update()
    if e in growth and e in grazing:# if experiment is a value and key in the dictionaries, add value to the key
        growth[station][e].update()
        grazing[station][e].update()
        net[station][e].update()
        growth_r2_value[station][e].update()
    elif e not in growth and e not in grazing:# if experiment is not a value and key in the dictionaries, create it
        growth[station][e] = {}
        grazing[station][e] = {}
        net[station][e]= {}
        r2_value[station][e] = {}
    if e in day_start: #if experiment key is part of the day_start list, add the follwing key:value pair as a value
        growth[station][e].update({'Start_time':'Daytime'})
        grazing[station][e].update({'Start_time': 'Daytime'})
        net[station][e].update({'Start_time': 'Daytime'})
    elif e in night_start: #if experiment key is a part of the night_start list, add the following key:value pair as a value
        growth[station][e].update({'Start_time':'Nighttime'})
        grazing[station][e].update({'Start_time': 'Nighttime'})
        net[station][e].update({'Start_time': 'Nighttime'})
    for t in time_rate: #for every item in the time_rate list
        m, b = np.polyfit(final_data['Fraction_whole_seawater'], final_data[t], 1) #creates regression line
        error = np.std(final_data[t]) / np.sqrt(len(final_data[t])) #calculates standard error
        st_error.append(error) #add standard error value to st_error list
        growth[station][e][t]= b #add time_rate:rate to growth inner most dictionary
        grazing[station][e][t]= -m #add time_rate:rate to grazing inner most dictionary
        net[station][e][t] = b - (-m) #adds time_rate:rate to net inner most dictionary
        corr_matrix = np.corrcoef(final_data['Fraction_whole_seawater'], final_data[t]) #next three lines calculate r2 value
        corr = corr_matrix[0, 1]
        R_sq = corr ** 2
        r2_value[station][e][t] = R_sq #adds time_rate:r2_value to the innermost dictionary

graph_actual_rates(growth) #graph growth rates
graph_actual_rates(grazing) #graph grazing rates
graph_actual_rates(net) #graph net rates


