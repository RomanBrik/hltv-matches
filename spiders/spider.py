from datetime import date, datetime as dt

import scrapy


class HltvItem(scrapy.Item):
    """Item object to store fields"""

    url  = scrapy.Field()
    team1 = scrapy.Field()
    score1 = scrapy.Field()
    team2 = scrapy.Field()
    score2 = scrapy.Field()
    winner = scrapy.Field()
    maps = scrapy.Field()
    stars = scrapy.Field()
    date = scrapy.Field()
    event = scrapy.Field()


# Crawler class
class HLTVSpider(scrapy.Spider):
    name = "hltv"
    allowed_domains = ['hltv.org']

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not start_date:
            start_date = date(date.today().year, 1, 1)

        if end_date:
            if end_date > date.today():
                end_date = date.today()
        else:
            end_date = date.today()

        self.start_urls = [
            f"https://www.hltv.org/results?startDate={start_date}&endDate={end_date}"
        ]
    
    def parse(self, response):
        matches = response.xpath(
            '//*[@class="results-all"]//*[@class="result-con"]'
        )
        for match in matches: 
            item = HltvItem()
            
            item['url'] = response.urljoin(match.xpath('a/@href').get())
            
            item['team1'] = match.xpath('(a//div[starts-with(@class, "team")])[1]/text()').get() 
             
            item['score1'] = int(
                match.xpath('a//span[contains(@class, "score")][1]/text()').get()
            ) 
            
            item['team2'] = match.xpath('(a//div[starts-with(@class, "team")])[2]/text()').get() 
            
            item['score2'] = int(
                match.xpath('a//span[contains(@class, "score")][2]/text()').get()
            ) 
            
            item['winner'] = match.xpath('a//div[contains(@class, "team-won")]/text()').get() 
                 
            item['maps'] = match.xpath('a//div[contains(@class, "map-text")]/text()').get() 
            
            item['stars'] = int(
                match.xpath('count(a//*[contains(@class, "fa fa-star star")])').get()[:-2]
            ) 
            # Date object
            item['date'] = dt.utcfromtimestamp(
                int(match.xpath('@data-zonedgrouping-entry-unix').get()[:-3])
            ).date()
            # str object
            item['event'] = match.xpath('a//span[@class="event-name"]/text()').get() 

            yield item
            
            # Next pages
            next_page = response.xpath('//a[@class="pagination-next"]/@href').get()
            
            if next_page is not None:
                yield response.follow(next_page)
