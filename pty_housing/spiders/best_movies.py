import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/chart/top/?ref_=nv_mv_250']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td[@class="titleColumn"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(), "Top Rated Indian Movies")]')),
    )

    def parse_item(self, response):
        item = dict()
        item['title'] = response.xpath('//h1[@class=""]/text()').get().replace('\xa0', '')
        item['year'] = response.xpath('//h1[@class=""]/span[@id="titleYear"]/a/text()').get()
        item['duration'] = response.xpath('normalize-space((//time)[1]/text())').get()
        item['genre'] = response.xpath('//div[@class="subtext"]/a[1]/text()').get()
        item['rating'] = response.xpath('//span[@itemprop="ratingValue"]/text()').get()
        item['director'] = response.xpath('//div[@class="credit_summary_item"]/h4[text()="Director:"]/following-sibling::a/text()').get()
        item['url'] = response.url
        yield item
