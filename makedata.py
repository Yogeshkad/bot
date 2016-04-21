import pandas as pd 
import numpy as np
from collections import defaultdict 
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score


#creat dataframe
df = pd.read_csv('data/matches.csv', parse_dates=["date"])
df.columns = ["date", "team1", "score1", "team2", "score2"]

#create winner column
df["1wins"] = df["score2"] < df["score1"]
y_true = df["1wins"].values

#create won_last columns that tell if a team won their last game
won_last = defaultdict(int)
df["team1LastWin"] = -1
df["team2LastWin"] = -1
for index, row in df.iterrows():	
	t1 = row["team1"]
	t2 = row["team2"]
	row["team1LastWin"] = won_last[t1]
	row["team2LastWin"] = won_last[t2]
	df.ix[index] = row
	won_last[t1] = row["1wins"]
	won_last[t2] = not row["1wins"]

last_match_winner = defaultdict(int)
dataset["team1WonLast"] = 0

for index, row in dataset.iterrows():
	team1 = row["Home Team"]
	team2 = row["Visitor Team"]
	teams = tuple(sorted([team1, team2]))
	row["team1WonLast"] = 1 if last_match_winner[teams] == row["Home Team"] else 0

# print df.head(5)
# print df.tail(5)
# f = open('yo.csv', 'w')
# df.to_csv(f)
# f.close()

clf = DecisionTreeClassifier(random_state=14)
X_previouswins = df[["team1LastWin", "team2LastWin"]].values
scores = cross_val_score(clf, X_previouswins, y_true, scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))