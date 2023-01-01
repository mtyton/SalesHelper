import pytest
from copy import deepcopy
from dataclasses import asdict
import uuid

from client.adapters import JobOfferListAdapter


def test_job_offer_list_adapter_success():
    offer = {
        "uuid": uuid.uuid4(),
        "title": "Some Job Offer",
        "skills": ["Python", "MongoDB"],
        "url": "https://mambojambo.com",
        "category": 3,
        "description": "SomeDescription"
    }
    adapter = JobOfferListAdapter()
    processed_offer = deepcopy(offer)
    processed_offer.pop("description")
    adapted_data = adapter.adapt(offer)
    assert adapted_data == processed_offer


def test_job_offer_list_adapter_invalid_data():
    offer = {
        "uuid": uuid.uuid4(),
        "title": "Some Job Offer",
        "skills": ["Python", "MongoDB"],
        "url": "https://mambojambo.com",
        "category": 3
    }
    adapter = JobOfferListAdapter()
    try:
        adapter.adapt(offer)
    except Exception as e:
        assert type(e) == TypeError




