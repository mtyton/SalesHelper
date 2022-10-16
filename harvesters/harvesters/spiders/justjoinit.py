import scrapy
import json


class JustjoinitSpider(
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
            skills = list(offer.get('skills'))
            yield {
                "link": link,
                "job_name": job_name,
                "company": company,
                "skills": {item['name']: item['level'] for item in skills}
            }
