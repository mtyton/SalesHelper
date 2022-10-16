import scrapy
import json

from harvesters.spiders.base import (
    DefaultPaginatedSpiderMixin,
    StopPaginationException
)


class JustjoinitSpider(
    DefaultPaginatedSpiderMixin,
    scrapy.Spider
):
    name = 'justjoinit'
    allowed_domains = ['justjoin.it']
    start_urls = ["https://justjoin.it/api/offers"]


    def parse(self, response):
        offers = json.loads(response.text)
        for offer in offers:
            link = "https://justjoin.it/offers/" + offer.get('id')
            job_name = offer.get('title')
            company = offer.get('company_name')
            yield {
                "link": link,
                "job_name": job_name,
                "company": company
            }
