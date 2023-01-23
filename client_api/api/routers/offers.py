from typing import List
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy import func

from api.schemas.offers import (
    JobOfferResponse,
    WrappedEmployeeResponse
)
from api.schemas.matches import (
    OfferMatchResponse,
    WrappedMatchResponse
)
from api.schemas.auth import UserResponse
from api.routers.auth import get_current_user
from client.main import dt_client
from database.db import get_db
from database.models import (
    EmployeeOfferMatch,
    EmployeeCategory,
    JobOffer
)


router = APIRouter(prefix="/offers")


@router.get("/", response_model=WrappedEmployeeResponse)
def get_job_offers(
    category: str, skip: int = 0, limit: int = 25,
    user: UserResponse=Depends(get_current_user),
    db=Depends(get_db),
):  
    if category == "all":
        data = db.query(JobOffer).offset(skip).limit(limit).all()
        count_query = db.query(func.count(JobOffer.id))
    else:
        numerical_category = getattr(EmployeeCategory, category).value
        data = db.query(JobOffer).filter(
            JobOffer.category==numerical_category
        ).offset(skip).limit(limit).all()
        count_query = db.query(
            func.count(JobOffer.id)
        ).filter(JobOffer.category==numerical_category)
    parsed_data = [
        JobOfferResponse.from_db_instance(job) for job in data
    ]
    response = WrappedEmployeeResponse(
        results=parsed_data, total_count=db.execute(count_query).first()[0]
    )
    return response


@router.get("/{offer_uuid}/match")
def get_offer_matched_employees(
    offer_uuid: UUID, skip: int=0, limit: int=25, db=Depends(get_db),
    user: UserResponse=Depends(get_current_user)
):
    matches = db.query(EmployeeOfferMatch).filter(
        EmployeeOfferMatch.offer_uuid==offer_uuid
    ).order_by(EmployeeOfferMatch.match_ratio.desc()).offset(skip).limit(limit).all()
    count_query = db.query(
        func.count(EmployeeOfferMatch.id)
    ).filter(EmployeeOfferMatch.offer_uuid==offer_uuid)
    response = WrappedMatchResponse(
        results=[OfferMatchResponse.from_db_instance(match) for match in matches],
        total_count=db.execute(count_query).first()[0]
    )
    return response