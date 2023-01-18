from fastapi import (
    APIRouter,
    Depends,
    BackgroundTasks
)
from typing import List
from sqlalchemy.orm import Session

from api.schemas.employees import (
    EmployeeResponse, 
    ResumeResponse,
    EmployeeRequest,
    ResumeAddRequest,
    ResumeUpdateRequest
)
from api.schemas.matches import EmployeeMatchResponse
from database.db import (
    get_db, 
    Base,
    engine
)
from database.models import (
    Employee,
    EmployeeOfferMatch
)
from database.tasks import synchronize_employee_matches
from api.routers.auth import get_current_user
from api.schemas.auth import UserResponse


router = APIRouter(prefix="/employees")


@router.get("/", response_model=List[EmployeeResponse])
def get_employees_list(
    skip: int = 0, limit:int = 25, db: Session = Depends(get_db),
    user: UserResponse=Depends(get_current_user)
):
    data = db.query(Employee).offset(skip).limit(limit).all()
    return [EmployeeResponse.from_db_instance(d) for d in data]


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_detail(
    employee_id: int, db: Session = Depends(get_db),
    user: UserResponse=Depends(get_current_user)
):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    return EmployeeResponse.from_db_instance(db_employee)


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    employee_data: EmployeeRequest, db: Session = Depends(get_db),
    user: UserResponse=Depends(get_current_user)
):
    db_instance = employee_data.insert(db)
    return EmployeeResponse.from_db_instance(db_instance)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_data: EmployeeRequest, db: Session = Depends(get_db),
    user: UserResponse=Depends(get_current_user)
):
    db_instance = employee_data.update(db)
    return EmployeeResponse.from_db_instance(db_instance)


@router.post("/{employee_id}/resume", response_model=ResumeResponse)
def create_employee_resume(
        employee_id: int, resume: ResumeAddRequest, bg_task: BackgroundTasks,  
        db: Session = Depends(get_db), user: UserResponse=Depends(get_current_user)
    ):
    instance = resume.insert(db, employee_id=employee_id)
    bg_task.add_task(synchronize_employee_matches, employee_id)
    return ResumeResponse.from_db_instance(instance)


@router.put("/{employee_id}/resume", response_model=ResumeResponse)
def create_employee_resume(
        employee_id: int, resume: ResumeUpdateRequest, bg_task: BackgroundTasks, 
        db: Session = Depends(get_db), user: UserResponse=Depends(get_current_user)
    ):
    instance = resume.update(db, employee_id=employee_id)
    employee = instance.owner
    employee.remove_matches()
    bg_task.add_task(synchronize_employee_matches, employee_id)
    return ResumeResponse.from_db_instance(instance)


@router.get("/{employee_id}/matches", response_model=List[EmployeeMatchResponse])
def get_employee_matches(
    employee_id: int, skip: int = 0, limit:int = 25, db: Session = Depends(get_db),
    user: UserResponse=Depends(get_current_user)    
):
    matches = db.query(EmployeeOfferMatch).filter(
        EmployeeOfferMatch.employee_id==employee_id
    ).offset(skip).limit(limit).all()
    return [EmployeeMatchResponse.from_db_instance(match) for match in matches]
