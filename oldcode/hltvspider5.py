#this spider scrapes data from hltv.org 
#it gets data from every match on the starting url
#and then recursively finds more pages of matches
from scrapy.crawler import CrawlerProcess
import scrapy
import csv
import re

#store matches as lists [date, team1, score1, team2, score2, pageid]
matches = []
rankings = {}
teams = {}

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

#filters from hltv stats page are represented in the start url. this spider scrapes 
#all matches from every page related to given filter
class HltvMatches(scrapy.Spider):
	name = 'matches'
	allowed_domains = ['hltv.org']
	start_urls = ['http://www.hltv.org/?pageid=188&statsfilter=5&offset=0']
	
	#overriding this method to use a Request() call
	#means the start url wont be revisted
	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url)		
	
	def parse(self, response):
		matchPath = """ 
			//div[@class="covMainBoxContent"]/div
			//div[@style = "width:606px;height:22px;background-color:white" 
			or @style = "width:606px;height:22px;background-color:#E6E5E5"]"""
		pagePath = '//div[@id="location"]/text()'
		#scrape match and page info
		page  = response.xpath(pagePath).extract()
		for div in response.xpath(matchPath):	
			data = []
			for index, text in enumerate(div.xpath('div/a/div/text()')):
				data.append(text.extract()) 					
			matches.append(textParser(data, page))
		#find other pages to visit
		for href in response.xpath('//div[@id="location"]/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse)	

#scrapes data on the top 30 ranked teams of each month given in start urls
class HltvRanks(scrapy.Spider):
	name = 'ranks'
	allowed_domains = ['hltv.org']
	start_urls = [['http://www.hltv.org/news/16983-team-ranking-january-2016', ['jan', 0]],
				['http://www.hltv.org/news/17225-team-ranking-february-2016', ['feb', 1]],
				['http://www.hltv.org/news/17488-team-ranking-march-2016', ['mar', 1]]]
	
	#override start_requests to pass meta variable 'month' containing
	#[dict key, month type] month type relates to changes in sites html over time
	def start_requests(self):
		for url in self.start_urls:		
			yield scrapy.Request(url[0], callback=self.parse, meta={'month': url[1]})				
	
	#gets ranking list from a page		
	def parse(self, response):
		ranking = []
		rankIndex = 1;
		month = response.meta['month']
		if month[1] == 0:
			path = """
				//table[@align = "center" and @style = "width: 90%;"]/tbody
				/tr[position()>1]/td[2]/span/strong/text()"""
		else:
			path = """
				//table[@align = "center" and @style = "width: 90%;"]/tbody
				/tr[position()>1]/td[2]/span/strong/a/text()"""
		for text in response.xpath(path):
			t = text.extract().encode('ascii', 'replace').strip(' ')
			teams[t] = True
			ranking.append([t, rankIndex])
			rankIndex += 1					
		rankings[month[0]] = ranking		

#takes scraped data and writes into a csv file
def createCsv(d):	
	if d == 'matches':
		fieldnames = ['date', 'team1', 'score1', 'team2', 'score2']
		fpath = 'data/matches/matches_all.csv'
		with open(fpath, 'w') as f:
			w = csv.DictWriter(f, fieldnames=fieldnames)
			w.writeheader()		
			w = csv.writer(f)	
			mSorted = sorted(matches,key=lambda x: x[5])
			for m in reversed(mSorted):
				m.pop()
				w.writerows([m])
	elif d == 'rankings': 
		fieldnames = ['team', 'rank']	
		for key in rankings:
			fpath = 'data/rankings/ranking_' + key + '.csv'
			with open(fpath, 'w') as f:
				w = csv.DictWriter(f, fieldnames=fieldnames)
				w.writeheader()		
				w = csv.writer(f)	
				for r in rankings[key]:
					w.writerows([r])
	elif d == 'teams':
		fieldnames = ['team']	
		fpath = 'data/teams.csv'
		with open(fpath, 'w') as f:
			w = csv.DictWriter(f, fieldnames=fieldnames)
			w.writeheader()		
			w = csv.writer(f)	
			for k in teams:
				w.writerows([[k]])	

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(HltvMatches)		
process.start()
createCsv('matches')

# process2 = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
# process2.crawl(HltvRanks)
# process2.start()
# createCsv('rankings')
# createCsv('teams')




