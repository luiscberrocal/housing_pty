from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from pty_housing.spiders.worldometer_corona import WorldometerCoronaSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(WorldometerCoronaSpider)
process.start()