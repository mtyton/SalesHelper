import pytest
import uuid
import requests_mock
from typing import List

from client.models import JobOffer
from client.main import (
    dt_client
)


@pytest.fixture(autouse=False)
def job_offers_list():
    return [{
        "uuid": str(uuid.uuid4()),
        "title": "Offer 1",
        "skills": ["Python", "MongoDB"],
        "url": "https://test.com",
        "category": 1,
        "description": "SomeDescription"
    }, {
        "uuid": str(uuid.uuid4()),
        "title": "Offer 2",
        "skills": ["C++", "SQL"],
        "url": "https://test2.com",
        "category": 1,
        "description": "Some boring description"
    }, {
        "uuid": str(uuid.uuid4()),
        "title": "Offer 3",
        "skills": ["C#", "Win-Forms"],
        "url": "https://test4.com",
        "category": 1,
        "description": "Final Interesting description"
    }, {
        "uuid": str(uuid.uuid4()),
        "title": "Offer 4",
        "skills": ["CSS", "React"],
        "url": "https://test5.com",
        "category": 2,
        "description": "Final Interesting description"
    }]


def test_data_service_client_get_job_offer_list_success_no_filters(job_offers_list):
    with requests_mock.Mocker() as m:
        m.get("http://data_service:5000/data/offers/", json=job_offers_list)
        job_offers = dt_client.get_job_offers_list(category="frontend")
    assert isinstance(job_offers, list)
    assert job_offers[0]["title"] == "Offer 1"
    assert job_offers[1]["title"] == "Offer 2"
    assert job_offers[2]["title"] == "Offer 3"


def test_data_service_client_get_job_offer_list_success_only_frontend_offers(job_offers_list):
    parsed_list = [elem for elem in job_offers_list if elem["category"] == 2]
    with requests_mock.Mocker() as m:
        m.get(
            "http://data_service:5000/data/offers/?skip=0&limit=25&category_name=frontend", 
            json=parsed_list
        )
        job_offers = dt_client.get_job_offers_list(category="frontend")
    assert isinstance(job_offers, list)
    assert len(job_offers) == 1
    assert job_offers[0]["title"] == "Offer 4"
    assert job_offers[0].get("description") is None
