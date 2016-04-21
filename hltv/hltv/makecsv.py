import csv
f = open('matches.csv', 'w')
fieldnames = ['date', 'team1', 'score1', 'team2', 'score2']
w = csv.DictWriter(f, fieldnames=fieldnames)
w.writeheader()