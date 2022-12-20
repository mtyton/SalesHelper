from dataclasses import (
    dataclass,
    asdict
)
from uuid import UUID
from bs4 import BeautifulSoup


@dataclass
class JobOffer:
    title: str
    skills: list
    url: str
    description: str
    platform: int
    uuid: UUID
    lang: str = None


@dataclass
class NERProcesableJobOffer:
    text: str
    uuid: UUID

    @classmethod
    def from_instance(cls, instance: JobOffer):
        text = instance.title +"\n"
        text += " ".join(instance.skills) + "\n"
        soup = BeautifulSoup(instance.description, features="lxml")
        description_text = soup.get_text(" ")
        text += description_text
        return cls(**{"text": text, "uuid": instance.uuid})
