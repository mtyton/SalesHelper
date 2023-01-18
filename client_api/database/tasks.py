from client.main import ml_client
from database.models import (
    Employee, 
    EmployeeOfferMatch
)
from database.db import get_db


MATCH_TRESHOLD = 0.3


def synchronize_employee_matches(employee_id: int) -> None:
    match_treshold = MATCH_TRESHOLD
    db = next(get_db())
    employee = db.query(Employee).filter(Employee.id==employee_id).first()
    if not employee:
        raise ValueError("Employee has not been found!")
    resume = employee.resume[0]
    if resume is None:
        raise ValueError("Employee has no resume uploaded")
    # start BackgroundTask
    for match_data in ml_client.get_match(employee=employee, resume_content=resume.content):
        if match_data["match_ratio"] >= match_treshold:
            employee.create_match(**match_data)
