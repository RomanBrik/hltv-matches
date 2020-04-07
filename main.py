import argparse
import logging
from datetime import datetime

from scrapy.crawler import CrawlerProcess

from spiders.spider import HLTVSpider
from settings import crawler_settings


SPIDER_LIST = [
    HLTVSpider,
]

parser = argparse.ArgumentParser(description='Crawler match data')
parser.add_argument('-start', '--s', action='store', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), dest='start_date')
parser.add_argument('-end', '--e', action='store', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), dest='end_date')

args = parser.parse_args()

start_date = args.start_date
end_date = args.end_date


if __name__ == "__main__":

    process = CrawlerProcess(settings=crawler_settings)

    for spider in SPIDER_LIST:
        process.crawl(spider, start_date, end_date)
    process.start()
