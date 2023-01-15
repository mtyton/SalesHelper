from dataclasses import (
    dataclass,
    asdict
)

from sqlalchemy.orm import Session
from database.db import Base
from database.models import (
    EmployeeCategory,
    Employee,
    Resume
)
from api.schemas.base import (
    DatabaseRequestBase,
    DatabaseResponseBase
)
from api.schemas.offers import JobOffer
from client.main import dt_client


@dataclass
class ResumeResponse(DatabaseResponseBase):
    content: str


@dataclass
class EmployeeResponse(DatabaseResponseBase):
    id: int
    name: str
    surname : str
    position: str

    is_busy: bool
    category: str
    resume: ResumeResponse
    
    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        mappings = {
            "category": str(EmployeeCategory(instance.category)).split(".")[-1]
        }

        resume = instance.resume[0] if instance.resume else None
        if resume:
            mappings["resume"] = ResumeResponse.from_db_instance(resume)
        else:
            mappings["resume"] = ResumeResponse(**{"content": ""})
        return mappings


@dataclass
class EmployeeRequest(DatabaseRequestBase):
    name: str
    surname : str
    position: str

    is_busy: bool
    category: int

    _model: Base = Employee

    def map_to_database_fields(self, db: Session, **kwargs):
        data = asdict(self)
        data.pop("_model")
        return data


@dataclass
class ResumeAddRequest(DatabaseRequestBase):
    content: str
    _model = Resume

    def map_to_database_fields(self, db: Session, **kwargs):
        employee_id = kwargs.pop("employee_id")
        return {
            "owner_id": employee_id,
            "content": self.content
        }


@dataclass
class ResumeUpdateRequest(ResumeAddRequest):
    def map_to_database_fields(self, db: Session, **kwargs):
        mapping = super().map_to_database_fields(db, **kwargs)
        employee = db.query(Employee).filter(Employee.id==mapping["owner_id"]).first()
        resume_id = employee.resume[0].id
        mapping["id"] = resume_id
        return mapping


@dataclass 
class EmployeeMatchResponse(DatabaseResponseBase):
    match_ratio: float
    offer: JobOffer

    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        offer_uuid = instance.offer_uuid
        offer_json = dt_client.get_exact_job_offer(offer_uuid)
        offer = JobOffer(**offer_json)
        return {
            "offer": offer
        }
