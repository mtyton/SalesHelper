import logging
from database.exceptions import ValidationError


logger = logging.getLogger("harvesterLogger")


class HarvestersPipeline:

    def process_item(self, item, spider):
        # Save only valid items into database
        try:
            item.insert_into_db()
        except ValidationError as e:
            logger.info(f"Issue occured during adding item: {item}, issue: {e}")

        return item
