from dataclasses import dataclass
from uuid import UUID


@dataclass
class JobOffer:
    uuid: UUID
    title: str
    skills: list
    url: str
    category: int
    platform: int
    lang: str
    description: str


@dataclass
class OfferMatchResponse:
    ...
