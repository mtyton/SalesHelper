from sqlalchemy import (
    Boolean, 
    Column, 
    ForeignKey, 
    Integer, 
    String, 
    Text
)
from sqlalchemy.orm import (
    relationship,
    Mapped
)
from enum import Enum
from uuid import UUID

from database.db import Base



class EmployeeCategory(Enum):
    backend = 1
    frontend = 2
    fullstack = 3
    mobile = 4


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String)
    surname: Mapped[str] = Column(String)
    position: Mapped[str] = Column(String)

    is_busy = Column(Boolean, default=False)
    resume = relationship("Resume", back_populates="owner")
    category: Mapped[EmployeeCategory] = Column(Integer)

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)

    owner_id = Column(Integer, ForeignKey("employees.id"))
    owner = relationship("Employee", back_populates="resume")


class EmployeeOfferMatch(Base):
    
    employee_id = Column(Integer, ForeignKey("employees.id"))
    employee = relationship("Employee", back_populates="matches")
    offer_uuid = Column(UUID(as_uuid=True))

    def get_offer_details(self):
        ...
