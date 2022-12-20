# This file contains definition of response/request models
from dataclasses import dataclass
from sqlalchemy.orm import Session

from database.db import Base
from database import models


class DatabaseResponseMixin:

    @classmethod
    def map_database_instance(cls, instance) -> dict:
        raise NotImplemented

    @classmethod
    def from_db_instance(cls, instance):
        if not instance:
            return None

        data = cls.map_database_instance(instance)
        return cls(**data)



class DatabaseRequestMixin:
    _model: Base = None

    def map_to_database_fields(self, db: Session):
        ...

    def save_to_db(self, db: Session):
        data = self.map_to_database_fields(db=db)
        instance = self._model(**data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance


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
class UserInfoBase:
    name: str
    surname: str
    position: str
    is_busy: bool


@dataclass
class UserInfo(DatabaseResponseMixin, UserInfoBase):

    @classmethod
    def map_database_instance(cls, instance) -> dict:
        data = {
            "name": instance.name,
            "surname": instance.surname,
            "position": instance.position,
            "is_busy": instance.is_busy
        }
        return data


@dataclass
class UserInfoDetail(UserInfo):
    resume: str

    @classmethod
    def map_database_instance(cls, instance) -> dict:
        data = super().map_database_instance(instance)
        data["resume"] = instance.resume.content
        return data


@dataclass
class UserInfoCreateRequest(DatabaseRequestMixin, UserInfoBase):
    _model = models.Employee
    
    def map_to_database_fields(self, db: Session):
        return {
            "name": self.name,
            "surname": self.surname,
            "position": self.position,
            "is_busy": self.is_busy
        }


@dataclass
class ResumeBase:
    content :str


@dataclass
class ResumeResponse(ResumeBase):
    user: str

    @classmethod
    def map_database_instance(cls, instance) -> dict:
        return {
            "user": instance.owner.full_name,
            "content": instance.content
        }


@dataclass
class ResumeCreateRequest(ResumeBase):
    user_id: int

    def map_to_database_fields(self, db: Session):
        employee = db.query(models.Employee).filter(user_id=self.user_id).first()
        return {
            "content": self.content,
            "owner_id": self.user_id,
            "owner": employee
        }