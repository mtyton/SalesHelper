from dataclasses import dataclass
from uuid import UUID


@dataclass
class ResumeMatchRequest:
    resume: str


@dataclass
class ResumeMatchResponse:
    offer_uuid: UUID
    match_ratio: float
