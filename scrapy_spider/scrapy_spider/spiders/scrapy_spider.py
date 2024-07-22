import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import re


SPIDER_DEPTH = 3


class SubdomainSpider(CrawlSpider):
    name = 'subdomain_spider'
    
    rules = (
        Rule(LinkExtractor(allow=(), unique=True), callback='parse_item', follow=True),
    )

    def __init__(self, allowed_domains=None, start_urls=None, spider_depth=SPIDER_DEPTH, *args, **kwargs):
        super(SubdomainSpider, self).__init__(*args, **kwargs)
        if allowed_domains:
            self.allowed_domains = allowed_domains
        if start_urls:
            self.start_urls = start_urls

        # visited urls as a key and visit number as value
        # also added +1 to visit number of one step above endpoint 
        self.visited_urls = dict()
        self.found_emails = set()

        self.email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    def parse_item(self, response):
        for link in LinkExtractor(allow=(), unique=True).extract_links(response):
            link.url = link.url.split('#')[0]

            if link.url in self.visited_urls.keys():
                continue

            parsed_url = urlparse(link.url)

            if parsed_url.hostname and any(parsed_url.hostname.endswith(domain) for domain in self.allowed_domains):
                # yield {'url': link.url}
                self.visited_urls[link.url] = 1

                above_url = '/'.join(link.url.split('/')[:-1]) + '/'

                if above_url in self.visited_urls:
                    if self.visited_urls[above_url] > SPIDER_DEPTH:
                        continue
                    self.visited_urls[above_url] += 1
                else:
                    self.visited_urls[above_url] = 1

                yield response.follow(link.url, self.parse_item)
        
        self.extract_emails(response)

    def extract_emails(self, response):
        emails = self.email_regex.findall(response.text)
        self.found_emails.update(emails)

    def closed(self, reason):
        with open('tmp/endpoints.txt', 'w') as f:
            f.write('\n'.join(self.visited_urls.keys()))
        with open('tmp/emails.txt', 'w') as f:
            f.write('\n'.join(self.found_emails))

        print(f"Spider closed: {reason}")
        print(f"Total emails found: {len(self.found_emails)}")
        print(f"URLs visited: {len(self.visited_urls)}")
        print(f"Emails and URLs saved to tmp directory")