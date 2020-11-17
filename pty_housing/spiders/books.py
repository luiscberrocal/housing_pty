import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//article[@class="product_pod"]/div/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a')),
    )

    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath('//h1/text()').get()
        item['price'] = response.xpath('//p[@class="price_color"]/text()').get()
        item['rating'] = response.xpath('//p[contains(@class, "star-rating")]/@class').get().replace('star-rating', '').strip()
        item['upc'] = response.xpath('//th[contains(text(), "UPC")]/following-sibling::td/text()').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield item
