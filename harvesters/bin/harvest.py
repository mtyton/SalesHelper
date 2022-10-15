from scrapy.crawler import CrawlerProcess


if __name__ == "__main__":
    # TODO - write script to automate launching crawling
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })
