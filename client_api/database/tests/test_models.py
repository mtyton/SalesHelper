import pytest
import uuid
from pytest import fixture
from sqlalchemy.exc import IntegrityError

from database.db import (
    Base,
    engine,
    get_db
)
from database import models


@fixture(autouse=True)
def db():
    Base.metadata.create_all(bind=engine)
    return next(get_db())


@fixture(autouse=False)
def employee(db):
    instance = models.Employee(**{
        "name": "Jerzy",
        "surname": "Test",
        "position": "Backend comedian",
        "is_busy": True,
        "category": 1
    })
    db.add(instance)
    db.commit()
    return instance


@fixture(autouse=False)
def resume(employee, db):
    resume = models.Resume(**{
        "owner_id": employee.id,
        "content": "SQL ,  SQL Server ,  Oracle ,  PL/SQL ,  jQuery ,  C# , \
        Windows Server ,  ETL ,  Java Script ,  Angielski ,  JavaScript ,  HTML ,  CSS "
    })
    db.add(resume)
    db.commit()
    return resume


@fixture(autouse=False)
def match(employee, db):
    match = models.EmployeeOfferMatch(**{
        "employee_id": employee.id,
        "offer_uuid": uuid.uuid4(),
        "match_ratio": 55.0
    })
    db.add(match)
    db.commit()
    # monkey patch
    match.get_offer_details = lambda x: "Details"
    return match


def test_create_match_success(employee):
    match_data = {
        "offer_uuid": uuid.uuid4(),
        "match_ratio": 96.0
    }
    match = employee.create_match(**match_data)
    assert match.id is not None
    assert match.match_ratio == match_data["match_ratio"]
    assert match.offer_uuid == match_data["offer_uuid"]


def test_create_match_missing_data(employee):
    match_data = {
        "offer_uuid": uuid.uuid4(),
    }
    try:
        employee.create_match(**match_data)
    except Exception as e:
        assert type(e) == IntegrityError


def test_remove_matches_success(match, db):
    employee = match.employee
    employee.remove_matches()
    matches = db.query(models.EmployeeOfferMatch).filter(models.EmployeeOfferMatch.employee_id==employee.id).all()
    assert len(matches) == 0
