import pandas as pd
import matplotlib.pyplot as plt
def mean_data(file, sheet, cols, group, avg): #avg refers to the variable which will be averaged
    data = pd.read_excel(file , sheet_name= sheet, usecols= cols)
    df = data.dropna()
    mean = df.groupby(group, as_index=False).agg(avg).mean()
    return mean

def graph(data, x, y):
    for grp, data in data.groupby('Cast #'):
        plt.plot(data[x], data[y], label= grp, marker='s', markersize=4)
    plt.gca().invert_yaxis()
    plt.xlabel(x, fontsize=14)
    plt.ylabel(y, fontsize=14)
    plt.grid(False)
    plt.style.use('ggplot')
    plt.legend()
    plt.show()
avg_data = mean_data('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx', 'Profiles', ['Cast #', 'Chl', 'Depth (m)'], ['Cast #', 'Depth (m)'], 'Chl')

print(avg_data)

graph(avg_data, 'Chl', 'Depth (m)')