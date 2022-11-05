from database.exceptions import ValidationError


class HarvestersPipeline:

    def process_item(self, item, spider):
        # Save only valid items into database
        try:
            item.insert_into_db()
        except ValidationError as e:
            # TODO - add logging here u dummy!
            ...

        return item
