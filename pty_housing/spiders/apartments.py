import re

import scrapy


class ApartmentsSpider(scrapy.Spider):
    name = 'apartments'
    allowed_domains = ['www.encuentra24.com']
    start_urls = ['http://www.encuentra24.com/panama-es/bienes-raices-venta-de-propiedades-apartamentos/']
    regexp = re.compile(
        r'^/(?P<country>[\w-]+)-(?P<lang>[\w-]+)/.*/(?P<slug>[\w-]+)/(?P<id>\d+)\?list=[\w-]+&catslug=(?P<category_slug>[\w-]+)')

    def parse(self, response):
        # link_xpath = "//article/div/span[4]/a[contains(@class, 'more-details')]"
        # link_xpath = "//article/div/span/a"
        link_xpath = "//article/div/span/a[contains(@class, 'more-details')]/@href"
        links = response.xpath(link_xpath).getall()
        link_data = dict()
        #link_data['page'] = 1
        #link_data['urls'] = list()
        for link in links:
            match = self.regexp.match(link)
            if match:
                url_data = dict()
                url_data['country'] = match.group('country')
                url_data['lang'] = match.group('lang')
                url_data['slug'] = match.group('slug')
                url_data['id'] = match.group('id')
                url_data['category_slug'] = match.group('category_slug')
                url_data['url'] = link
                #link_data['urls'].append(url_data)

                yield url_data

    def _specific_data(self, response):
        xpath = "//li/span[@class='info-name']/ancestor::ul"
        infos = response.xpath("//li/span[@class='info-name']")
        name = infos[1].xpath('./text()').get()
        value_data = infos[1].xpath('./following-sibling::node()/text()').get()

