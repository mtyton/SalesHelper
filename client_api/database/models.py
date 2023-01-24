from typing import Union
from sqlalchemy import (
    Boolean, 
    Column, 
    ForeignKey, 
    Integer, 
    String, 
    Text,
    Float,
    JSON
)
from sqlalchemy.orm import (
    relationship,
    Mapped
)
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID

from database.db import (
    Base,
    get_db
)


class EmployeeCategory(Enum):
    backend = 1
    frontend = 2
    fullstack = 3
    mobile = 4


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    username: Mapped[str] = Column(String)
    password: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String)


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String)
    surname: Mapped[str] = Column(String)
    position: Mapped[str] = Column(String)

    is_busy = Column(Boolean, default=False)
    category: Mapped[int] = Column(Integer)
    
    resume = relationship("Resume", back_populates="owner")
    matches = relationship("EmployeeOfferMatch", back_populates="employee")

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

    def create_match(self, **match_kwargs) -> Union[None, Base]:
        match_kwargs["employee_id"] = self.id
        db = next(get_db())
        if db.query(EmployeeOfferMatch).filter(
            EmployeeOfferMatch.offer_uuid==match_kwargs["offer_uuid"],
            EmployeeOfferMatch.employee_id==self.id
        ).first():
            return
        instance = EmployeeOfferMatch(**match_kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        db.close()
        return instance

    def remove_matches(self) -> None:
        db = next(get_db())
        db.query(EmployeeOfferMatch).filter(EmployeeOfferMatch.employee_id==self.id).delete()
        db.commit()
        db.close()


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)

    owner_id = Column(Integer, ForeignKey("employees.id"))
    owner = relationship("Employee", back_populates="resume")


class EmployeeOfferMatch(Base):
    __tablename__ = "employeeoffersmatches"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    employee = relationship("Employee", back_populates="matches")
    
    offer_uuid = Column(UUID(as_uuid=True), nullable=False)
    match_ratio = Column(Float, nullable=False)


class JobOffer(Base):
    __tablename__ = "joboffers"

    id = Column(Integer, primary_key=True, index=True)
    offer_uuid = Column(UUID(as_uuid=True), nullable=False)
    title = Column(Text)
    skills = Column(JSON)
    url = Column(Text)
    category = Column(Integer)
    platform = Column(Integer)
    lang = Column(Text)
    description = Column(Text)
