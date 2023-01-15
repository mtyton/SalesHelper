from typing import List
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends
)

from api.schemas.offers import (
    JobOffer,
    OfferMatchResponse
)

from client.main import dt_client
from database.db import get_db
from database.models import EmployeeOfferMatch


router = APIRouter(prefix="/offers")


@router.get("/", response_model=List[JobOffer])
def get_job_offers(category: str, skip: int = 0, limit: int = 25):
    data = dt_client.get_job_offers_list(category=category, skip=skip, limit=limit)
    return [
        JobOffer(**kw) for kw in data
    ]


@router.get("/{offer_uuid}", response_model=JobOffer)
def get_job_offer(offer_uuid: UUID):
    return JobOffer(
        **dt_client.get_exact_job_offer(offer_uuid)
    )


@router.get("/{offer_uuid}/match")
def get_offer_matched_employees(offer_uuid: UUID, skip: int=0, limit: int=25, db=Depends(get_db)):
    matches = db.query(EmployeeOfferMatch).filter(
        EmployeeOfferMatch.offer_uuid==offer_uuid
    ).offset(skip).limit(limit).all()
    return [OfferMatchResponse.from_db_instance(match) for match in matches]
