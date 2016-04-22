from scrapy.crawler import CrawlerProcess as cp
from spiders.hltv_ranks import spider as rankSpider
from spiders.hltv_matches import spider as matchSpider

process = cp({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
#process.crawl(rankSpider)		
process.crawl(matchSpider)
process.start()
