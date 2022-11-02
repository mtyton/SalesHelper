# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass
from enum import Enum

from uuid import UUID


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
