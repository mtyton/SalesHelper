from dataclasses import (
    dataclass,
    asdict
)
from uuid import UUID


@dataclass
class JobOffer:
    uuid: UUID
    title: str
    skills: list
    url: str
    category: int
    description: str


@dataclass
class JobOfferList:
    uuid: UUID
    title: str
    skills: list
    url: str
    category: int

    @classmethod
    def from_instance(cls, instance: JobOffer):
        data = asdict(instance)
        data.pop("description", None)
        return cls(**data)
