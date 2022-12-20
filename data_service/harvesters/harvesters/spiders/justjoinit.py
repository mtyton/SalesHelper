import scrapy
import json
from scrapy import http
from bson.binary import Binary

from harvesters.encryptor import encrypt_uuid
from harvesters.items import (
    JobOffer,
    JobPlatforms
)

class JustjoinitSpider(scrapy.Spider):
    name = 'justjoinit'
    allowed_domains = ['justjoin.it']
    start_urls = [
        "https://justjoin.it/api/offers",
        'https://justjoin.it/offers/'
    ]

    def _extract_uuid(self, offer_id):
        return encrypt_uuid(offer_id)

    def parse_details(self, response):
        offer = json.loads(response.text)
        offer_id = str(offer.get('id'))
        title = str(offer.get('title'))
        desc = str(offer.get('body'))
        skills = list(offer.get('skills'))
        url = "https://justjoin.it/api/offers/" + offer_id
        yield JobOffer(**{
            "title": title,
            "skills": skills,
            "url": url,
            "description": desc,
            "platform": JobPlatforms.JUSTJOINIT.value,
            "uuid": Binary.from_uuid(self._extract_uuid(offer_id))
        })

    def parse(self, response):
        offers = json.loads(response.text)
        for offer in offers:
            url = "https://justjoin.it/api/offers/" + str(offer.get('id'))
            yield http.Request(url=url, callback=self.parse_details)
