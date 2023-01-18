import logging
from database.exceptions import (
    ValidationError,
    DocumentAlreadyExistsException
)
from database.models import JobOfferDocument


logger = logging.getLogger("harvesterLogger")


class HarvestersPipeline:

    def process_item(self, item, spider):
        # Save only valid items into database
        uuid = item["uuid"]
        try:
            document = JobOfferDocument()
            item = document.insert(**item)
        except ValidationError as e:
            logger.info(f"Issue occured during adding item: {uuid}, issue: {e}")
        except DocumentAlreadyExistsException as e:
            logger.info(f"Document: {uuid} already exists in database")

        return item
