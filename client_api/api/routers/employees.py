from fastapi import (
    APIRouter,
    Depends
)
from typing import List

from api.schemas.employees import (
    EmployeeResponse, 
    ResumeResponse,
    EmployeeRequest,
    ResumeAddRequest
)
from database.db import (
    get_db, 
    Base,
    engine
)
from database.models import (
    Employee
)
from sqlalchemy.orm import Session


router = APIRouter(prefix="/employees")


@router.get("/", response_model=List[EmployeeResponse])
def get_employees_list(db: Session = Depends(get_db)):
    data = db.query(Employee).offset(1).limit(10).all()
    return [EmployeeResponse.from_db_instance(d) for d in data]


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_detail(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    return EmployeeResponse.from_db_instance(db_employee)


@router.post("/", response_model=EmployeeResponse)
def create_employee(employee_data: EmployeeRequest, db: Session = Depends(get_db)):
    db_instance = employee_data.insert(db)
    return EmployeeResponse.from_db_instance(db_instance)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_data: EmployeeRequest, db: Session = Depends(get_db)):
    db_instance = employee_data.update(db)
    return EmployeeResponse.from_db_instance(db_instance)


@router.post("/{employee_id}/resume", response_model=ResumeResponse)
def create_employee_resume(employee_id: int, resume: ResumeAddRequest, db: Session = Depends(get_db)):
    instance = resume.insert(db, employee_id=employee_id)
    return ResumeResponse.from_db_instance(instance)


@router.put("/{employee_id}/resume", response_model=ResumeResponse)
def create_employee_resume(employee_id: int, resume: ResumeAddRequest, db: Session = Depends(get_db)):
    instance = resume.update(db, employee_id=employee_id)
    return ResumeResponse.from_db_instance(instance)
