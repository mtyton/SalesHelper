from dataclasses import dataclass

from database.db import Base
from schemas.offers import JobOffer
from schemas.employees import EmployeeResponse
from api.schemas.base import DatabaseResponseBase
from client.main import dt_client


@dataclass 
class EmployeeMatchResponse(DatabaseResponseBase):
    match_ratio: float
    offer: JobOffer

    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        offer_uuid = instance.offer_uuid
        offer_json = dt_client.get_exact_job_offer(offer_uuid)
        offer = JobOffer(**offer_json)
        return {
            "offer": offer
        }

@dataclass
class OfferMatchResponse(DatabaseResponseBase):
    match_ratio: float
    employee: EmployeeResponse
    
    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        employee = instance.employee
        return {
            "employee": EmployeeResponse.from_db_instance(employee)
        }
