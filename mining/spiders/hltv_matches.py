from scrapy import Spider
from scrapy import Request
import util

#store matches as lists [date, team1, score1, team2, score2, pageid]
matches = {'lan':[], 'onl':[], 'both':[]} 

#built in filters from hltv are represented in the start urls. 
class spider(Spider):
	name = 'matches'
	allowed_domains = ['hltv.org']
	start_urls = [['http://www.hltv.org/?pageid=188&statsfilter=2053&offset=0', 'lan'],
				['http://www.hltv.org/?pageid=188&statsfilter=1797&offset=0', 'onl'],
				['http://www.hltv.org/?pageid=188&statsfilter=5&offset=0', 'both']]
	
	#overriding this method to use a Request() call
	#means the start url wont be revisted and meta 'matchType' can be passed
	def start_requests(self):
		for url in self.start_urls:
			request = Request(url[0], meta={'matchType': url[1]})		
			yield request
		
	#creates a CSV for each match type
	def closed(self, reason):
		util.createMatchCsv('lan', matches['lan'])
		util.createMatchCsv('onl', matches['onl'])
		util.createMatchCsv('both', matches['both'])
		
	def parse(self, response):
		matchPath = """ 
			//div[@class="covMainBoxContent"]/div
			//div[@style = "width:606px;height:22px;background-color:white" 
			or @style = "width:606px;height:22px;background-color:#E6E5E5"]"""
		pagePath = '//div[@id="location"]/text()'
		page  = response.xpath(pagePath).extract()
		matchType = response.meta['matchType']
		#get match data
		for div in response.xpath(matchPath):	
			data = []
			for index, text in enumerate(div.xpath('div/a/div/text()')):
				data.append(text.extract()) 					
			matches[matchType].append(util.textParser(data, page))
		#find other pages to visit
		for href in response.xpath('//div[@id="location"]/a/@href'):
			url = response.urljoin(href.extract())
			yield Request(url, callback=self.parse, meta=response.meta)	

