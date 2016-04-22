import scrapy


class HltvSpider(scrapy.Spider):
	name = "hltv0"
	allowed_domains = ["hltv.org"]
	start_urls = ["http://www.hltv.org/?pageid=188&statsfilter=5/"]
	
	def parse(self, response):
		mainbox = response.selector.xpath('//div[@class="covMainBoxContent"]/div')
		for div in mainbox.xpath('div'):
			#for a in div.xpath('div').xpath('a'):
			# for a in div.xpath('div/a'):
			# 	print a.xpath('')
			for ref in div.xpath('div/a/div/text()'):
				print ref.extract()
				print '-------------------'

			print '    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  '


		# for d in enumerate(mainbox):
		# 	print d.xpath()


	# def parse(self, response):
	# 	hxs = HtmlXPathSelector(response)
	# 	#titles = hxs.select('//div[@class="covMainBoxContent"]')
	# 	titles = hxs.select("//p")
	# 	for title in titles: 
	# 		item = HltvItem()
	# 		item["title"] = titles.select("a/text()").extract()
	# 		link = titles.select("a/@href").extract()
	# 		print titles, link




# class DmozSpider(scrapy.Spider):
#     name = "dmoz"
#     allowed_domains = ["dmoz.org"]
#     start_urls = [
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
#     ]

#     def parse(self, response):
#         filename = response.url.split("/")[-2] + '.html'
#         with open(filename, 'wb') as f:
#             f.write(response.body)

			  				
				  	