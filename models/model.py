import pandas as pd 
import numpy as np
from collections import defaultdict 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.grid_search import GridSearchCV
import csv

teams = {}
ranks = {}	
match_dfs = {}


months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
r_months = ['jan', 'feb', 'mar']
mTypes = ['onl', 'lan', 'both']
fieldnames = ['date', 'team1', 'score1', 'team2', 'score2']

print '>'

#get teams
with open('../data/teams/teams_all.csv', mode='r') as f:
	reader = csv.reader(f)
	teams = dict((row[0], True) for row in reader)

#get ranks
for m in r_months:
	with open('../data/ranks/ranks_' + m + '.csv', mode='r') as f:
		data = {}
		reader = csv.reader(f)
		data = dict((row[0], row[1]) for row in reader)	
		ranks[m] = defaultdict(lambda: 99, data)

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

always_ranked_teams = teams.copy()
for m in r_months:
	for t in always_ranked_teams:
				if t not in data:
					always_ranked_teams = removekey(always_ranked_teams, t)



#creat match dataframes
for t in mTypes:
	tdf = pd.read_csv('../data/matches/' + t + '_matches_all.csv', parse_dates=['date'])
	tdf = tdf[tdf.date >= np.datetime64('2016-02-01')] 
	match_dfs[t] = tdf





#df = df_mar.append(df_apr, ignore_index=True)

print 'lan'
df = match_dfs['lan']
#rank = ranks['feb']


df = df[df.team1.isin(always_ranked_teams)]
df = df[df.team2.isin(always_ranked_teams)]

##~~~~~~~~~~~~~~~~~~~~~~~
# for index, row in df.iterrows():
# 	print row

# for k in rank:
# 	print k, ' ', rank[k]
##~~~~~~~~~~~~~~~~~~~~~~~


#create winner column
df['1wins'] = df['score2'] < df['score1']
y_true = df['1wins'].values

#create won_last columns that tell if a team won their last game
won_last = defaultdict(int)
df['team1LastWin'] = 0
df['team2LastWin'] = 0
for index, row in df.iterrows():	
	t1 = row['team1']
	t2 = row['team2']
	row['team1LastWin'] = won_last[t1]
	row['team2LastWin'] = won_last[t2]
	df.ix[index] = row
	won_last[t1] = row['1wins']
	won_last[t2] = not row['1wins']

#find who won when the teams previously played
# last_match_winner = defaultdict(int)
# df['team1WonLast'] = 0
# for index, row in df.iterrows():
# 	t1 = row['team1']
# 	t2 = row['team2']
# 	teams = tuple(sorted([t1, t2]))
# 	row['team1WonLast'] = 1 if last_match_winner[teams] == row['team1'] else 0
# 	df.ix[index] = row
#   	winner = row["team1"] if row["1wins"] else row["team2"]
#   	last_match_winner[teams] = winner

#ranking 
df["team1RanksHigher"] = 0
for index, row in df.iterrows():
	t1 = row["team1"]
	t2 = row["team2"]
	date = row["date"]
	month = months[date.month-2 % 12]
	t1_rank = ranks[month][t1] 
	t2_rank = ranks[month][t2]
	row["team1RanksHigher"] = int(t1_rank) < int(t2_rank)
	df.ix[index] = row    

# df["team1LastRankHigher"] = 0
# df["team2LastRankHigher"] = 0
# for index, row in df.iterrows():
# 	t1 = row["team1"]
# 	t2 = row["team2"]
# 	date = row["date"]
# 	month = months[date.month-2 % 12]
# 	t1_rank = ranks[month][t1] 
# 	t2_rank = ranks[month][t2]

# 	row["team1LastRankHigher"] = int(t1_rank) < int(t2_rank)
# 	row["team2LastRankHigher"] = int(t2_rank) < int(t1_rank)
# 	df.ix[index] = row   
# 	#print '----------'
	
	#print month, t1, t2, t1_rank, t2_rank, row["team1LastRankHigher"], row["team2LastRankHigher"]


for index, row in df.iterrows():	
	
	if row.date < np.datetime64('2016-03-01'):
		print row
		print '		----'




X_home_higher = df[['team1LastWin', 'team2LastWin', 'team1LastRankHigher', 'team2LastRankHigher']].values 

encoding = LabelEncoder()
encoding.fit(df["team1"].values)

t1s = encoding.transform(df["team1"].values)
t2s = encoding.transform(df["team2"].values)
X_teams = np.vstack([t1s, t2s]).T

onehot = OneHotEncoder()
X_teams_expanded = onehot.fit_transform(X_teams).todense()
X_all = np.hstack([X_home_higher, X_teams])


parameter_space = {
	"max_features": [2, 5, 'auto'],
	"n_estimators": [100,],
	"criterion": ["gini", "entropy"],
	"min_samples_leaf": [2, 4, 6],
}
clf = RandomForestClassifier(random_state=14)
grid = GridSearchCV(clf, parameter_space)
grid.fit(X_all, y_true)
print("Accuracy: {0:.1f}%".format(grid.best_score_ * 100))
#----------------------------------------------

#X =  df[['team1WonLast', 'team1RanksHigher']].values

#X = df[['team1LastWin', 'team2LastWin', 'team1RanksHigher']].values ##>>>>>>>>>>>>>>>>>  #68.5 <<<<<<<<<<<<<<<<<<<<<<<<<

#X = df[['team1LastWin', 'team2LastWin', 'team1LastRankHigher', 'team2LastRankHigher']].values 

# X = df[['team1LastWin', 'team2LastWin', 'team1WonLast']].values
#X = onehot.fit_transform(X_teams).todense()
#X = X_teams_expanded

#----------------------------------------------
#clf = DecisionTreeClassifier(random_state=14)
#clf = RandomForestClassifier(random_state=14)

#----------------------------------------------
#scores = cross_val_score(clf, X, y_true, scoring='accuracy')
#print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))



