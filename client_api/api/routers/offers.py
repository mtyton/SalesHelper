from typing import List
from uuid import UUID
from fastapi import APIRouter

from api.schemas.offers import (
    JobOffer,
    JobOfferDetails
)
from client.main import dt_client


router = APIRouter(prefix="/offers")


@router.get("/", response_model=List[JobOffer])
def get_job_offers(category: str, skip: int = 0, limit: int = 25):
    data = dt_client.get_job_offers_list(category=category, skip=skip, limit=limit)
    print(data)
    return [
        JobOffer(**kw) for kw in data
    ]


@router.get("/{offer_uuid}", response_model=JobOfferDetails)
def get_job_offer(offer_uuid: UUID):
    return JobOfferDetails(
        **dt_client.get_exact_job_offer(offer_uuid)
    )


@router.get("/{offer_uuid}/match")
def get_offer_matched_employees(offer_uuid: UUID):
    ...
