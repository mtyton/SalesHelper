from dataclasses import dataclass
from uuid import UUID
from typing import List


@dataclass
class RawEntryResponseModel:
    title: str
    skills: list
    url: str
    description: str
    platform: int
    uuid: UUID
    lang: str = None


@dataclass
class NlpProcessedData:
    text: str
    uuid: UUID
    ents: list

    @classmethod
    def from_db_instance(cls, instance):
        data = {
            "text": instance["text"],
            "uuid": instance["tre"],
            "ents": instance.ents
        }
        return cls(**data)


@dataclass
class DoccanoAnnotatedData:
    text: str
    entities: List[dict]


@dataclass
class TrainingData:
    ...
