import scrapy


class KnivesSpider(scrapy.Spider):
    name = 'knives'
    allowed_domains = ['www.bladehq.com/cat--Manual-Knives--45']
    start_urls = ['http://www.bladehq.com/cat--Manual-Knives--45/']

    def parse(self, response):
        xpath ="//div[@class='itemDetails']"
        item_details = response.xpath(xpath)
        for item in item_details:
            pass


