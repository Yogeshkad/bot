from scrapy import Spider
from scrapy import Request
import util

ranks = {}
teams = {}

#scrapes data on the top 30 ranked teams of each month given in start urls
class spider(Spider):
	name = 'ranks'
	allowed_domains = ['hltv.org']
	start_urls = [['http://www.hltv.org/news/16983-team-ranking-january-2016', ['jan', 0]],
				['http://www.hltv.org/news/17225-team-ranking-february-2016', ['feb', 1]],
				['http://www.hltv.org/news/17488-team-ranking-march-2016', ['mar', 1]]]
	
	#override start_requests to pass meta variable 'month' containing
	#[dict key, month type] month type relates to changes in sites html over time
	def start_requests(self):
		for url in self.start_urls:		
			yield Request(url[0], callback=self.parse, meta={'month': url[1]})				
	
	def closed(self, reason):
		util.createRankCsv(ranks)
		util.createTeamCsv(teams)

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
		ranks[month[0]] = ranking	

