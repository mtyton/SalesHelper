from pydantic import BaseModel
from uuid import UUID


class RawEntryResponseModel(BaseModel):
    title: str
    skills: list
    url: str
    description: str
    platform: int
    uuid: UUID
    lang: str = None


class NlpProcessedRequestData(BaseModel):
    text: str
    uuid: UUID
    ents: list
