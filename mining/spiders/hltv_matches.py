from scrapy import Spider
from scrapy import Request
import util

#store matches as lists [date, team1, score1, team2, score2, pageid]
matches = []

#filters from hltv stats page are represented in the start url. this spider scrapes 
#all matches from every page related to given filter
class spider(Spider):
	#matches = []
	name = 'matches'
	allowed_domains = ['hltv.org']
	start_urls = ['http://www.hltv.org/?pageid=188&statsfilter=5&offset=0']
	
	#overriding this method to use a Request() call
	#means the start url wont be revisted
	def start_requests(self):
		for url in self.start_urls:
			yield Request(url)		
	
	def closed(self, reason):
		util.createCsv('matches', matches)

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
			matches.append(util.textParser(data, page))
		#find other pages to visit
		for href in response.xpath('//div[@id="location"]/a/@href'):
			url = response.urljoin(href.extract())
			yield Request(url, callback=self.parse)	

