import scrapy
from scrapy import http

from harvesters.spiders.base import (
    DefaultPaginatedSpiderMixin,
    StopPaginationException
)


class NofluffjobsSpider(
    DefaultPaginatedSpiderMixin, 
    scrapy.Spider
):
    name = 'nofluffjobs'
    allowed_domains = ['nofluffjobs.com']
    start_urls = ["https://nofluffjobs.com/pl/backend"]

    
    def _get_next_page_url(self, response):
        next = response.css("a.page-link::attr(href)").getall()
        url = next[-1]
        page_number = int(url.split("?page=")[-1])
        if page_number == self.current_page_number:
            raise StopPaginationException
        return url 


    def parse(self, response):
        offers = response.css("a.posting-list-item")
        for offer in offers:
            link = offer.css("::attr(href)").get()
            job_name = offer.css("h3::text").get()
            company = offer.css("span.posting-title__company::text").get()
            yield {
                "link": link,
                "job_name": job_name,
                "company": company
            }
        try:
            url = self._get_next_page_url(response)
            url = response.urljoin(url)
        except StopPaginationException:
            yield
        yield http.Request(url=url, callback=self.parse)
