import pandas as pd
import matplotlib.pyplot as plt
def mean_data(file, sheet, group): #avg refers to the variable which will be averaged
    data = pd.read_excel(file , sheet_name=sheet)
    df = data.groupby(group, as_index=False, dropna=True)
    mean = df.mean()
    return mean

def graph(data, group, x, y):
    for grp, data in data.groupby(group):
        plt.plot(data[x], data[y], label= grp, marker='s', markersize=4)
    plt.gca().invert_yaxis()
    plt.xlabel(x, fontsize=14)
    plt.ylabel(y, fontsize=14)
    plt.grid(False)
    plt.style.use('ggplot')
    plt.legend(title=group)
    plt.show()


avg_data = mean_data('C:\\Users\\Luis\\Research\\Chlorophyll\\Chlorophyll_Data.xlsx', 'Profiles', ['Cast #', 'Depth (m)'])

print(avg_data)

graph(avg_data, 'Cast #', 'Chl', 'Depth (m)')

