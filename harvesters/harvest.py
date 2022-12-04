from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from harvesters.harvesters.spiders import (
    NofluffjobsSpider,
    JustjoinitSpider
)
from harvesters.harvesters import settings as my_settings


SPIDERS_CLASSES = [
    NofluffjobsSpider,
    JustjoinitSpider
]


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(crawler_settings)
    process.crawl(NofluffjobsSpider)
    process.start()
