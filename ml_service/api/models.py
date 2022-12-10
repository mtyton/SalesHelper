from dataclasses import dataclass


@dataclass
class ResumeMatchRequest:
    text: str


@dataclass
class ResumeMatchResponse:
    title: str
    skills: list
    url: str
    description: str
