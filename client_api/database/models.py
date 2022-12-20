from sqlalchemy import (
    Boolean, 
    Column, 
    ForeignKey, 
    Integer, 
    String, 
    Text
)
from sqlalchemy.orm import relationship

from database.db import Base
    

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    position = Column(String)

    is_busy = Column(Boolean, default=False)
    resume = relationship("Resume", back_populates="owner")

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)

    owner_id = Column(Integer, ForeignKey("employees.id"))
    owner = relationship("Employee", back_populates="resume")
