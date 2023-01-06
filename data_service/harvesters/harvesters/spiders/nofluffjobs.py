import scrapy
from scrapy import http
from urllib.parse import urljoin
from bson.binary import Binary

from harvesters.spiders.base import (
    DefaultPaginatedSpiderMixin,
    StopPaginationException
)
from harvesters.encryptor import encrypt_uuid
from database.schemas import (
    JobOffer,
    JobPlatforms,
    OfferCategories
)
from tools import detect_description_language


class NofluffjobsSpider(
    DefaultPaginatedSpiderMixin, 
    scrapy.Spider
):
    name = 'nofluffjobs'
    allowed_domains = ['nofluffjobs.com']
    start_urls = [
        # "https://nofluffjobs.com/pl/backend",
        "https://nofluffjobs.com/pl/frontend",
        "https://nofluffjobs.com/pl/fullstack",
        "https://nofluffjobs.com/pl/mobile",
    ]

    def _get_next_page_url(self, response):
        next = response.css("a.page-link::attr(href)").getall()
        url = next[-1]
        page_number = int(url.split("?page=")[-1])
        if page_number == self.current_page_number:
            raise StopPaginationException
        return url 

    def _extract_uuid(self, url):
        return encrypt_uuid(url.split("-")[-1])

    def parse_details(self, response):
        skill_block = response.css("div#posting-requirements")
        skills_ul = skill_block.css("ul.mb-0")
        skills = skills_ul.css("li > span::text").getall()
        description = response.css("nfj-read-more > div").extract_first()
        title = response.css("h1::text").extract_first()
        category = response.css("a.font-weight-semi-bold::text").extract_first().strip()
        lang = detect_description_language(description)
        yield {
            "title": title,
            "skills": skills, 
            "url": response.url,
            "description": description,
            "platform": JobPlatforms.NOFLUFFJOBS.value,
            "uuid": self._extract_uuid(response.url),
            "category": OfferCategories.from_text(category),
            "lang": lang
        }

    def parse(self, response):
        offers = response.css("a.posting-list-item")
        for offer in offers:
            link = offer.css("::attr(href)").get()
            detail_url = urljoin(response.url, link)
            yield http.Request(url=detail_url, callback=self.parse_details)
        try:
            url = self._get_next_page_url(response)
            url = response.urljoin(url)
        except StopPaginationException:
            yield
        yield http.Request(url=url, callback=self.parse)
