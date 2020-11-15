import scrapy


class CigabuySpider(scrapy.Spider):
    name = 'cigabuy'
    allowed_domains = ['www.cigabuy.com']
    start_urls = ['http://www.cigabuy.com/specials.html']

    def parse(self, response):
        #//div[@id='productListing']/div[@class='r_b_c']/div[@class='p_box_wrapper']
        xpath ="//ul[@class='productlisting-ul']/div[@class='p_box_wrapper']/div"
        products_divs = response.xpath(xpath)
        for product in products_divs:
            price = product.xpath(".//div[@class='p_box_price cf']/span[1]/text()").get()
            reg_price = product.xpath(".//div[@class='p_box_price cf']/span[2]/text()").get()
            if price is None:
                price = product.xpath(".//div[@class='p_box_price cf']/text()").get()

            product_dict = dict()
            product_dict['name'] = product.xpath("./a[@class='p_box_title']/text()").get()
            product_dict['url'] = product.xpath("./a[@class='p_box_title']/@href").get()
            product_dict['price'] = price
            product_dict['regular_price'] = reg_price
            yield product_dict

        next_page = response.xpath("(//a[@class='nextPage'])[1]/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

