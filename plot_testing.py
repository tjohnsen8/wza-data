from matplotlib import pyplot
import pandas as pd
import csv
from wza_data import data_dir

wod_headers = ['WOD 1', 'WOD 2', 'WOD 3', 'WOD 4', 'WOD 5', 'WOD 6', 'WOD 7']

# get the two divisons i want
elite = pd.read_csv(f'{data_dir}elite_men.csv', sep=',', header=0)
interm = pd.read_csv(f'{data_dir}int_men.csv', sep=',', header=0)

# get the workout data
elite_res = []
int_res = []
for header in wod_headers:
	elite_res.append(elite.loc[:,header][elite.loc[:,header] > 0])
	int_res.append(interm.loc[:,header][interm.loc[:,header] > 0])

# remove outliers
for ind in range(0, len(wod_headers)):
	elite_res[ind] = elite_res[ind][(elite_res[ind] - elite_res[ind].mean()) <= 3*elite_res[ind].std()]
	int_res[ind] = int_res[ind][(int_res[ind] - int_res[ind].mean()) <= 3*int_res[ind].std()]

# now plot the wods
for ind in range(0, len(wod_headers)):
	pyplot.hist(elite_res[ind], bins='auto', alpha=0.9, label=f'elite\n{elite_res[ind].describe()}')
	pyplot.hist(int_res[ind], bins='auto', alpha=0.9, label=f'int\n{int_res[ind].describe()}')
	pyplot.legend(loc='upper right')
	pyplot.show()