import scrapy
import json


class NofluffjobsSpiderDetails(scrapy.Spider):
    name = 'nofluffjobs_details'
    allowed_domains = ['nofluffjobs.com']
    start_urls = ['http://nofluffjobs.com/pl']

    def parse_details(self, response):
        skill_block = response.css("div#posting-requirements")
        skills_ul = skill_block.css("ul.mb-0")
        skills = skills_ul.css("li > span::text").getall()

        yield {"skills": skills, "url": response.url}


    def parse(self, response):
        with open("data/nofluffjobs.json") as f:
            raw_data = f.read()
            parsed_data = json.loads(raw_data)
    
        for d in parsed_data:
            url = response.urljoin(d["link"])
            yield scrapy.Request(url=url, callback=self.parse_details)
