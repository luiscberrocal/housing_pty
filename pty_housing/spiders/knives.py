import scrapy
from scrapy_splash import SplashRequest


class KnivesSpider(scrapy.Spider):
    name = 'knives'
    allowed_domains = ['www.bladehq.com']

    script = '''
    function main(splash, args)
      splash.private_mode_enabled = false
      assert(splash:go(args.url))
      assert(splash:wait(0.5))
      splash:set_viewport_full()
      return {
        html = splash:html(),
        --png = splash:png(),
        --har = splash:har(),
      }
    end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.bladehq.com/cat--Manual-Knives--45",
                            callback=self.parse, endpoint="execute", args={
                'lua_source': self.script
            })

    def parse(self, response):
        xpath = "//div[@class='itemDetails']"
        item_details = response.xpath(xpath)
        for item in item_details:
            knife = dict()
            knife['name'] = item.xpath('.//a/div[contains(@class, "itemName")]/text()').get()
            knife['price'] = item.xpath('.//a/div[contains(@class, "itemPrice")]/span/div[@class="price"]/span/text()').get()
            knife['url'] = item.xpath('.//a[1]/@href').get()
            yield knife


