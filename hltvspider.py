#this spider scrapes data from hltv.org 
#it gets data from every match on the starting url
#and then recursively finds more pages of matches
from scrapy.crawler import CrawlerProcess
import scrapy
import csv
import re

#store matches as lists [date, team1, score1, team2, score2, pageid]
matches = []

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

#this class does all of the scraping and crawling
class HltvSpider(scrapy.Spider):
	name = "hltv"
	allowed_domains = ["hltv.org"]
	start_urls = ["http://www.hltv.org/?pageid=188&statsfilter=5&offset=0"]
	#overriding this method to use a Request() call
	#means the start url wont be revisted 
	
	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url)		
	
	def parse(self, response):
		#scrape match info from a page
		page = response.xpath('//div[@id="location"]/text()').extract()
		mainbox = response.xpath('//div[@class="covMainBoxContent"]/div')
		for div in mainbox.xpath("""
			//div[@style = "width:606px;height:22px;background-color:white" 
			or @style = "width:606px;height:22px;background-color:#E6E5E5"]"""):
			data = []
			for index, text in enumerate(div.xpath('div/a/div/text()')):
				data.append(text.extract()) 					
			matches.append(textParser(data, page))
		#find other pages to visit
		for href in response.xpath('//div[@id="location"]/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse)	

#clear txt file and create new csv
# def clearFile():	
# 	f = open('matches.csv', 'w')
# 	fieldnames = ['date', 'team1', 'score1', 'team2', 'score2']
# 	w = csv.DictWriter(f, fieldnames=fieldnames)
# 	w.writeheader()
# 	f.close()

#sorts matches and puts them in a csv
def createCsv():
	
	mSorted = sorted(matches,key=lambda x: x[5])
	with open('data/matches.csv', 'w') as f:
		fieldnames = ['date', 'team1', 'score1', 'team2', 'score2']
		w = csv.DictWriter(f, fieldnames=fieldnames)
		w.writeheader()		
		w = csv.writer(f)
		for m in reversed(mSorted):
			m.pop()
			w.writerows([m])
	
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(HltvSpider)		
process.start()
createCsv()


