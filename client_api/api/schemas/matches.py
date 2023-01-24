from dataclasses import dataclass
from typing import (
    Union,
    List
)

from database.db import Base
from schemas.offers import JobOfferResponse
from schemas.employees import EmployeeResponse
from api.schemas.base import DatabaseResponseBase
from client.main import dt_client

@dataclass 
class EmployeeMatchResponse(DatabaseResponseBase):
    match_ratio: float
    offer: JobOfferResponse

    def __post_init__(self, *args, **kwargs):
        self.match_ratio = round(self.match_ratio, 4)

    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        offer_uuid = instance.offer_uuid
        offer_json = dt_client.get_exact_job_offer(offer_uuid)
        offer = JobOfferResponse(**offer_json)
        return {
            "offer": offer
        }

@dataclass
class OfferMatchResponse(DatabaseResponseBase):
    match_ratio: float
    employee: EmployeeResponse
    
    def __post_init__(self, *args, **kwargs):
        self.match_ratio = round(self.match_ratio, 4)

    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        employee = instance.employee
        return {
            "employee": EmployeeResponse.from_db_instance(employee)
        }


@dataclass
class WrappedMatchResponse:
    
    results: Union[List[OfferMatchResponse], List[EmployeeMatchResponse]]
    total_count: int = 0
