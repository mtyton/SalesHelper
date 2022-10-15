import scrapy
import json

from harvesters.spiders.base import (
    DetailSpiderMixin
)



class NofluffjobsSpiderDetails(
    DetailSpiderMixin,
    scrapy.Spider
):
    name = 'nofluffjobs_details'
    allowed_domains = ['nofluffjobs.com']
    
    basic_url = "http://nofluffjobs.com/pl"
    list_data_filename = "data/nofluffjobs.json"

    def parse_details(self, response):
        skill_block = response.css("div#posting-requirements")
        skills_ul = skill_block.css("ul.mb-0")
        skills = skills_ul.css("li > span::text").getall()
        yield {"skills": skills, "url": response.url}
