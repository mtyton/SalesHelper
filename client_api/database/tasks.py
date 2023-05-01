from client.main import ml_client
from database.models import (
    Employee, 
    EmployeeOfferMatch
)
from database.db import get_db
from database.commands.download_job_offers import create_job_offer


MATCH_TRESHOLD = 0.3


def synchronize_employee_matches(employee_id: int) -> None:
    match_treshold = MATCH_TRESHOLD
    db = next(get_db())
    employee = db.query(Employee).filter(Employee.id==employee_id).first()
    if not employee:
        raise ValueError("Employee has not been found!")
    try:
        resume = employee.resume[0]
    except IndexError:
        raise ValueError("Employee has no resume uploaded")
    # start BackgroundTask
    
    for match_data in ml_client.get_match(employee=employee, resume_content=resume.content):
        if match_data["match_ratio"] >= match_treshold:
            match = employee.create_match(**match_data)
            if match is not None:
                create_job_offer(match)
    
