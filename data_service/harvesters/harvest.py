import argparse

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from harvesters.spiders import (
    NofluffjobsSpider
)
from harvesters import settings as my_settings


SPIDERS_MAPPING = {
    "nofluffjobs": NofluffjobsSpider
}

import logging

logger = logging.getLogger("harvesterLogger")
logger.setLevel(logging.DEBUG)

ch = logging.FileHandler("harvest.log")
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


def run(crawler):
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(crawler_settings)
    logger.info(f"Starting Crawling for {crawler}")
    process.crawl(crawler)
    process.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Data harvesters",
        description="Harvest data from available job offers websites. \
            This data will be used to train nlp model",
    )
    parser.add_argument(
        "website", choices=list(SPIDERS_MAPPING.keys())
    )
    args = parser.parse_args()
    run(SPIDERS_MAPPING[args.website])
