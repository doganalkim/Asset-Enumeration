from scrapy.crawler import CrawlerProcess

from scrapy_spider.scrapy_spider.spiders.scrapy_spider import SubdomainSpider
from config import SPIDER_DEPTH


class EndpointScanTools:
    # outputs to <domain>.txt file
    def scrapy(self, allowed_domains: list, start_urls: list):
        process = CrawlerProcess()
        process.crawl(SubdomainSpider, allowed_domains=allowed_domains, start_urls=start_urls, spider_depth=SPIDER_DEPTH)
        process.start()
      

# To-do: abandon process feature
#        when ctrl+^d pressed

# for testing purposes
if __name__=='__main__':
    est = EndpointScanTools()
    est.scrapy(allowed_domains=['toscrape.com'], start_urls=['https://quotes.toscrape.com'])