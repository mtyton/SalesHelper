from dataclasses import (
    dataclass,
    asdict
)
from bson.binary import Binary
from uuid import UUID
from enum import Enum


class OfferCategories(Enum):
    backend = 1
    frontend = 2
    fullstack = 3
    mobile = 4

    # TODO - this can be refactored!!
    @classmethod
    def from_text(cls, text: str) -> Enum:
        text = text.lower()
        return getattr(cls, text).value


class JobPlatforms(Enum):
    NOFLUFFJOBS = 1
    JUSTJOINIT = 2


class OfferLanguages(Enum):
    PL = "PL"
    EN = "EN"


class DatabaseSchemaBase:

    def get_database_dict(self):
        return asdict(self)

    @classmethod
    def from_db_instance(cls, **kwargs):
        kwargs.pop("_id", None)
        return cls(**kwargs)


class UUIDHandleMixin:
    def get_database_dict(self):
        data = super().get_database_dict()
        data["uuid"] = Binary.from_uuid(self.uuid)
        return data

    @classmethod
    def from_db_instance(cls, **kwargs):
        kwargs["uuid"] = kwargs["uuid"].as_uuid()
        return super().from_db_instance(**kwargs)


@dataclass
class JobOffer(UUIDHandleMixin, DatabaseSchemaBase):
    title: str
    skills: list
    url: str
    description: str
    platform: JobPlatforms
    uuid: UUID
    lang: str
    category: OfferCategories = None


@dataclass
class DoccanoData(UUIDHandleMixin, DatabaseSchemaBase):
    text: str
    uuid: UUID
    ents: list


@dataclass
class TrainingData(DatabaseSchemaBase):
    text:str
    ents: list
