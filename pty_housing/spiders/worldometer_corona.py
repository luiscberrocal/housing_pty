import scrapy
import logging

class WorldometerCoronaSpider(scrapy.Spider):
    name = 'worldometer_corona'
    allowed_domains = ['www.worldometers.info/coronavirus']
    start_urls = ['http://www.worldometers.info/coronavirus/']
    column_mappings = {
        3: 'total_cases',
        4: 'new_cases',
        5: 'total_deaths',
        6: 'new_deaths',
        7: 'total_recovered',
        9: 'active_cases',
        10: 'serious_critical',
        11: 'cases_x_million',
        12: 'deaths_x_million',
        13: 'total_tests',
        14: 'test_x_million',
    }

    def parse(self, response):
        xpath ="//table[@id='main_table_countries_today']/tbody[1]/tr"
        xpath = "//table[@id='main_table_countries_today']/tbody[1]/tr/td/a[@class='mt_a']"
        #//div[@id='productListing']/div[@class='r_b_c']/div[@class='p_box_wrapper']
        links = response.xpath("//table[@id='main_table_countries_today']/tbody[1]/tr/td/a[@class='mt_a']")


        for link in links:
            country_data = dict()
            name = link.xpath('./text()').get()
            country_data['country'] = name
            logging.info(f'{name}')
            tr = link.xpath("./ancestor::tr")

            columns = tr.xpath("./td")
            col_num = 1
            for col in columns:
                value = col.xpath('./text()').get()
                if col_num in self.column_mappings.keys():
                    country_data[self.column_mappings[col_num]] = value
                else:
                    logging.info(f'NOT MAPPED Name {col_num}: {value}')
                col_num += 1
            logging.info('>'*15)
            yield country_data


