import click
from scrapy.crawler import CrawlerProcess

from scrapy_spider.scrapy_spider.spiders.scrapy_spider import SubdomainSpider
from config import SPIDER_DEPTH
from main import _save_endpoints


class EndpointScanTools:
    # outputs to endpoints.txt file
    def scrapy(self, allowed_domains: list, start_urls: list):
        process = CrawlerProcess()
        process.crawl(SubdomainSpider, allowed_domains=allowed_domains, start_urls=start_urls, spider_depth=SPIDER_DEPTH)
        process.start()


@click.command()
@click.option('--url', required=True, help='URL(s) to spider. Separated by commas.')
@click.option('--allowed_domains', required=True, help='A list of domains separated by commas. '
                                                       'Spider will only visit the links in these domains.')
def entry(url, allowed_domains):
    url = url.replace(' ', '').split(',')
    allowed_domains = allowed_domains.replace(' ', '').split(',')

    est = EndpointScanTools()
    est.scrapy(allowed_domains=allowed_domains, start_urls=url)

    _save_endpoints('_'.join(allowed_domains))

# for testing purposes
if __name__=='__main__':
    entry()
    # est = EndpointScanTools()
    # est.scrapy(allowed_domains=['toscrape.com'], start_urls=['https://quotes.toscrape.com'])