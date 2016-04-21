import csv
import pandas as pd 
import numpy as np

fieldnames = ['date', 'team1', 'score1', 'team2', 'score2']
months = [['feb', '2016-01-31', '2016-03-01'], 
			['mar', '2016-02-29', '2016-04-01'],
			['apr', '2016-03-31', '2016-05-01']]

df = pd.read_csv('data/matches.csv', parse_dates=["date"])
df.columns = fieldnames

def writeMonthCsv(name, start, end):
	with open('data/' + name + '.csv', 'w') as f:
		w = csv.DictWriter(f, fieldnames=fieldnames)
		w.writeheader()	
		w = csv.writer(f)
		for index, row in df.iterrows():
			if (row['date'] > np.datetime64(start)) and (row['date'] < np.datetime64(end)):
				w.writerows([row])

for m in months:
 	writeMonthCsv(m[0], m[1], m[2])


