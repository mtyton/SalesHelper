from dataclasses import dataclass
from uuid import UUID
from typing import List

from api.schemas.base import DatabaseResponseBase
from database.db import Base


@dataclass
class JobOfferResponse(DatabaseResponseBase):
    uuid: UUID
    title: str
    skills: list
    url: str
    category: int
    platform: int
    lang: str
    description: str

    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        return {
            "uuid": instance.offer_uuid
        }


@dataclass
class WrappedEmployeeResponse:
    results: List[JobOfferResponse]
    total_count: int = 0
