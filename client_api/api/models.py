# This file contains definition of response/request models
from dataclasses import dataclass


@dataclass
class JobOffer:
    # TODO - uuid should of type uuid not str
    uuid: str
    title: str
    skills: list
    url: str


@dataclass
class JobOfferDetails(JobOffer):
    description: str


@dataclass
class UserInfo:
    name: str
    surname: str
    year_of_experience: int
    position: int
    is_busy: bool


@dataclass
class UserInfoDetail(UserInfo):
    resume_id: str

    def get_resume_content(self):
        # TODO - this is a placeholder
        return "Resume Resume Resume Resume"
