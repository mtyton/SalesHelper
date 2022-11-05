# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from dataclasses import asdict
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from database.db import conn


class HarvestersPipeline:

    def process_item(self, item, spider):
        # TODO accept only english job offers
        existing_entry = conn.collection.find_one({"uuid": item.uuid})
        if existing_entry:
            return item

        conn.collection.insert_one(asdict(item))
        return item
