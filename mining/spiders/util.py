import csv
import re
import os

#converts raw text to csv usable list
def textParser(data, page):
	d =[]
	#parse date
	day, month, year = re.split(r'[/\s]\s*', data[0])
	if len(month) == 1:
		month = '0' + month
	if len(day) == 1:
		day = '0' + day			
	d.append('20' + year + '-' + month + '-' + day)
	#parse team data
	for i in range(1,3):
		team, score = data[i].encode('ascii', 'replace').split('(')
		d.append(team.lstrip(' ').rstrip(' '))
		d.append(score.strip(')'))
	#parse page number			
	p = ''.join(page)
	p = p.encode('ascii', 'ignore') 			
	p = ''.join(c for c in p if c.isdigit())
	d.append(int(p))
	return d;

#takes scraped data and writes into a csv file
def createCsv(d, data):	
	if d == 'matches':
		fpath = '../data/matches/matches_all.csv'
		fieldnames = ['date', 'team1', 'score1', 'team2', 'score2']
		with open(fpath, 'w') as f:
			w = csv.DictWriter(f, fieldnames=fieldnames)
			w.writeheader()		
			w = csv.writer(f)	
			mSorted = sorted(data,key=lambda x: x[5])
			for m in reversed(mSorted):
				m.pop()
				w.writerows([m])
	elif d == 'ranks': 
		fieldnames = ['team','rank']	
		for key in data:
			fpath = '../data/ranks/ranks_' + key + '.csv'
			with open(fpath, 'w') as f:
				w = csv.DictWriter(f, fieldnames=fieldnames)
				w.writeheader()		
				w = csv.writer(f)	
				for r in data[key]:
					w.writerows([r])
	elif d == 'teams':
		fpath = '../data/teams/teams_all.csv'
		fieldnames = ['team']	
		with open(fpath, 'w') as f:
			w = csv.DictWriter(f, fieldnames=fieldnames)
			w.writeheader()		
			w = csv.writer(f)	
			for k in data:
				w.writerows([[k]])	