import logging
import re

import scrapy


class ApartmentsSpider(scrapy.Spider):
    name = 'apartments'
    allowed_domains = ['www.encuentra24.com']
    start_urls = ['http://www.encuentra24.com/panama-es/bienes-raices-venta-de-propiedades-apartamentos/']
    regexp = re.compile(
        r'https://www.encuentra24.com/(?P<country>[\w-]+)-(?P<lang>[\w-]+)/.*/(?P<slug>[\w-]+)/(?P<id>\d+)\?list=[\w-]+&catslug=(?P<category_slug>[\w-]+)')

    columns = {
        'M² de construcción': {'name': 'area'},
        'M2': {'name': 'area_m2'},
        'Recámaras': {'name': 'rooms'},
        'Precio': {'name': 'price'},
        'Año de construcción': {'name': 'construction_date'},
        'Piscina': {'name': 'pool'},
        'Categoria': {'name': 'category'},
        'Enviado': {'name': 'post_date'},
        'Localización': {'name': 'location'},
        'Dirección exacta': {'name': 'address'},
        'Parking': {'name': 'parkings'},
        'Baños': {'name': 'bathrooms'},
        'Altura': {'name': 'height'},
        'Tipo de pisos': {'name': 'floor_type'},
        'Tamaño del lote': {'name': 'lot_size'},
        'Balcón/Terraza': {'name': 'balcony'},
        'Niveles': {'name': 'levels'},
        'Precio/M² de construcción': {'name': 'price_x_sq_meter'},

    }

    def parse(self, response):
        # link_xpath = "//article/div/span[4]/a[contains(@class, 'more-details')]"
        # link_xpath = "//article/div/span/a"
        link_xpath = "//article/div/span/a[contains(@class, 'more-details')]/@href"
        links = response.xpath(link_xpath).getall()
        link_data = dict()
        # link_data['page'] = 1
        # link_data['urls'] = list()
        for link in links:
            match = self.regexp.match(link)
            if match:
                yield response.follow(url=link, callback=self.parse_apartment)

    def parse_apartment(self, response):

        current_url = response.url
        xpath = "//li/span[@class='info-name']"
        infos = response.xpath(xpath)
        housing_data = dict()
        match = self.regexp.match(current_url)

        if match:
            housing_data['country'] = match.group('country')
            housing_data['lang'] = match.group('lang')
            housing_data['slug'] = match.group('slug')
            housing_data['id'] = match.group('id')
            housing_data['category_slug'] = match.group('category_slug')
            housing_data['url'] = current_url
        else:
            housing_data['country'] = 'UNKOWN'
            housing_data['url'] = current_url

        for info in infos:

            name = info.xpath('./text()').get().replace(':', '').strip()
            value_data = info.xpath('./following-sibling::node()/text()').get()
            column= self.columns.get(name)
            if column:
                housing_data[column['name']] = value_data
                #logging.info(f'{name} ({self.columns[name]["name"]}): {value_data}')
            else:
                logging.info(f'MISSING {name} : {value_data}')
        yield housing_data
