import json

from urllib.parse import urljoin
from scrapy import http


class StopPaginationException(Exception):
    ...


class DefaultPaginatedSpiderMixin:
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_page_number = 1

    def _get_next_page_url(self, response):
        ...


class DetailSpiderMixin:

    list_data_filename = None
    detail_url_key = "link"
    basic_url = None

    def parse_details(self, response):
        ...

    def start_requests(self):
        if not self.list_data_filename or not self.basic_url:
            return
        with open(self.list_data_filename, "r") as f:
            parsed_data = json.load(f)
        for elem in parsed_data:
            url = urljoin(self.basic_url, elem[self.detail_url_key])
            yield http.Request(url=url, callback=self.parse_details)
