import scrapy


class NofluffjobsSpider(scrapy.Spider):
    name = 'nofluffjobs'
    allowed_domains = ['nofluffjobs.com']
    start_urls = ['http://nofluffjobs.com/pl']

    def parse(self, response):
        offers = response.css("a.posting-list-item")
        data = []
        for offer in offers:
            link = offer.css("::attr(href)").get()
            job_name = offer.css("h3::text").get()
            company = offer.css("span.posting-title__company::text").get()
            yield {
                "link": link,
                "job_name": job_name,
                "company": company
            }