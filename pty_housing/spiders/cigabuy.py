import scrapy
import re

class CigabuySpider(scrapy.Spider):
    name = 'cigabuy'
    allowed_domains = ['www.cigabuy.com']
    start_urls = ['http://www.cigabuy.com/specials.html']
    star_regex = re.compile(r's_star_(?P<num>\d)_?(?P<dec>\d)?')

    def parse(self, response):
        #//div[@id='productListing']/div[@class='r_b_c']/div[@class='p_box_wrapper']
        xpath ="//ul[@class='productlisting-ul']/div[@class='p_box_wrapper']/div"
        products_divs = response.xpath(xpath)
        for product in products_divs:
            price = product.xpath(".//div[@class='p_box_price cf']/span[1]/text()").get()
            reg_price = product.xpath(".//div[@class='p_box_price cf']/span[2]/text()").get()
            if price is None:
                price = product.xpath(".//div[@class='p_box_price cf']/text()").get()
            stars = product.xpath(".//div[@class='p_box_star']/span/@class").get()
            match = self.star_regex.search(stars)
            if match:
                num = match\
                    .group('num')
                dec = match.group('dec') or '0'
                stars = f'{num}.{dec}'
            else:
                stars =None
            product_dict = dict()
            product_dict['name'] = product.xpath("./a[@class='p_box_title']/text()").get()
            product_dict['url'] = product.xpath("./a[@class='p_box_title']/@href").get()
            product_dict['price'] = price
            product_dict['regular_price'] = reg_price
            product_dict['stars'] = stars
            #product_dict['agent'] = response.request.headers['User-Agent']
            yield scrapy.Request(url= product_dict['url'], callback=self.parse_product,
                                 meta=product_dict)

        next_page = response.xpath("(//a[@class='nextPage'])[1]/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        product_dict = response.meta
        xpath = "//span[contains(text(), 'SKU')]/following-sibling::strong/text()"
        product_dict['sku'] = response.xpath(xpath).get()
        yield product_dict


