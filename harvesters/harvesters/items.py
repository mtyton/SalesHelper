# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dataclasses import (
    dataclass,
    asdict
)
from enum import Enum
from uuid import UUID

from database.db import conn
from database.exceptions import ValidationError
from nlp.tools import detect_description_language


SUPPORTED_OFFERS_LANGUAGES = [
    "PL", "EN"
]


class JobPlatforms(Enum):
    NOFLUFFJOBS = 1
    JUSTJOINIT = 2


@dataclass
class JobOffer:
    title: str
    skills: list
    url: str
    description: str
    platform: JobPlatforms
    uuid: UUID
    lang: str = None

    def __post_init__(self, *args, **kwargs):
        self.lang = detect_description_language(self.description)

    # TODO - consider raise ValidationError
    def is_valid(self) -> bool:
        existing_entry = conn.collection.find_one({"uuid": self.uuid})
        if existing_entry:
            return False
        # Check if offer language is supported
        if not self.lang in SUPPORTED_OFFERS_LANGUAGES:
            return False
        return True

    def insert_into_db(self, force_insert: bool=False) -> None:
        if not self.is_valid():
            raise ValidationError(
                message="This item is inavlid it is not possible to insert it into database."
            )
        conn.collection.insert_one(asdict(self))
