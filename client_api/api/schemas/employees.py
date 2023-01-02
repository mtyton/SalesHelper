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


@dataclass
class ResumeResponse(DatabaseResponseBase):
    content: str


@dataclass
class EmployeeListResponse(DatabaseResponseBase):
    id: int
    name: str
    surname : str
    position: str

    is_busy: bool
    category: str

    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        return {
            "category": str(EmployeeCategory(instance.category)).split(".")[-1]
        }


@dataclass 
class EmployeeDetailResponse(EmployeeListResponse):
    resume: ResumeResponse

    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        mappings = super().special_field_mappings(instance)
        mappings["resume"] = ResumeResponse.from_db_instance(instance.resume)
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
        data["category"] = EmployeeCategory(data["category"])
        return data


@dataclass
class ResumeAddRequest(DatabaseRequestBase):
    content: str

    def map_to_database_fields(self, db: Session, **kwargs):
        employee_id = kwargs.pop("employee_id")
        employee = db.query(Employee).filter(id=employee_id)
        return {
            "owner_id": employee_id,
            "owner": employee,
            "content": self.content
        }
