from typing import List
from uuid import UUID
from fastapi import APIRouter

from api.schemas.offers import (
    JobOffer,
    JobOfferDetails
)


router = APIRouter(prefix="/offers")


@router.get("/", response_model=List[JobOffer])
def get_job_offers():
    # TODO - it should look for data in data_service
    return [
        JobOffer(
            **{"title": "Test`1", "skills": ["C++", "Python"], "url": "https://fastapi.com", "uuid": "1"}
        ),
        JobOffer(
            **{"title": "Test`2", "skills": ["C#", "Java"], "url": "https://fastapi.com", "uuid": "2"}
        ),
    ]


@router.get("/{offer_uuid}", response_model=JobOfferDetails)
def get_job_offer(offer_uuid: UUID):
    return JobOfferDetails(
        **{
            "title": "Test`1", "skills": ["C++", "Python"], "url": "https://fastapi.com", 
            "uuid": str(offer_uuid), "description": "This is a test job offer description, it'll get longer soon"
        }
    )


@router.get("/{offer_uuid}/match")
def get_offer_matched_employees(offer_uuid: UUID):
    ...
