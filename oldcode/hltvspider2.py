import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import re
import textwrap

#this spider will go to a stats page on hltv and grab every available match data
#it will then recursively find other pages to visit and grab the match data there
#untill it has visited every page of matches
class HltvSpider(scrapy.Spider):
	name = "hltv"
	allowed_domains = ["hltv.org"]
	start_urls = ["http://www.hltv.org/?pageid=188&statsfilter=5&offset="]
	
	
	def start_requests(self):
    	for url in self.start_urls:
            for i in range(50):
            	try:
            		#yield self.make_requests_from_url(url + str(i*50))		
                	yield Request(url + str(i*50), meta={'priority': index})
           		except:
           			continue



	def parse(self, response):
		
		#converts raw text to csv usable list
		def textParser(data):
			d =[]
			day, month, year = re.split(r'[/\s]\s*', data[0])
			if len(month) == 1:
				month = '0' + month
			if len(day) == 1:
				day = '0' + day			
			d.append('20' + year + '-' + month + '-' + day)
			team1, score1 = data[1].split('(')
			team2, score2 = data[2].split('(')
			d.append(team1.lstrip(' ').rstrip(' '))
			d.append(score1.strip(')'))
			d.append(team2.lstrip(' ').rstrip(' '))
			d.append(score2.strip(')'))
			return d;
		
		f = open('matches.csv', 'a')
		w = csv.writer(f)

		#scrape match info
		mainbox = response.xpath('//div[@class="covMainBoxContent"]/div')
	
		for div in mainbox.xpath("""
			//div[@style = "width:606px;height:22px;background-color:white" 
			or @style = "width:606px;height:22px;background-color:#E6E5E5"]"""):
		
			data = []
			for index, text in enumerate(div.xpath('div/a/div/text()')):
				data.append(text.extract().encode('ascii', 'replace')) 					
			w.writerows([textParser(data)])

			

		#find other pages to visit
		for href in response.xpath('//div[@id="location"]/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse)

		f.close()

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

f = open('matches.csv', 'w')
fieldnames = ['date', 'team1', 'score1', 'team2', 'score2']
w = csv.DictWriter(f, fieldnames=fieldnames)
w.writeheader()
f.close()

process.crawl(HltvSpider)		
process.start()



