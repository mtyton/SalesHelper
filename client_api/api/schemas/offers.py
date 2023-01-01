from dataclasses import dataclass
from uuid import UUID


@dataclass
class JobOffer:
    uuid: UUID
    title: str
    skills: list
    url: str
    category: int


@dataclass
class JobOfferDetails(JobOffer):
    description: str
