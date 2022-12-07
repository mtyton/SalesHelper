from typing import List

from fastapi import FastAPI
from api import models as rmodels



app = FastAPI()


@app.get("/offers", response_model=List[rmodels.JobOffer])
def get_job_offers():
    # TODO - it should look for data in data_service
    return [
        rmodels.JobOffer(
            **{"title": "Test`1", "skills": ["C++", "Python"], "url": "https://fastapi.com", "uuid": "1"}
        ),
        rmodels.JobOffer(
            **{"title": "Test`2", "skills": ["C#", "Java"], "url": "https://fastapi.com", "uuid": "2"}
        ),
    ]


@app.get("/offers/{offer_uuid}", response_model=rmodels.JobOfferDetails)
def get_job_offers(offer_uuid):
    return rmodels.JobOfferDetails(
        **{
            "title": "Test`1", "skills": ["C++", "Python"], "url": "https://fastapi.com", 
            "uuid": str(offer_uuid), "description": "This is a test job offer description, it'll get longer soon"
        }
    )


@app.get("/users", response_model=List[rmodels.UserInfo])
def get_users_list():
    return [
        rmodels.UserInfo(name="john", surname="Kowalski", year_of_experience=10, position="Senior Dev", is_busy=False),
        rmodels.UserInfo(name="john", surname="Kowalski", year_of_experience=10, position="Senior Dev", is_busy=False)
    ]


@app.get("/users/{user_id}", response_model=rmodels.UserInfoDetail)
def get_user_details(user_id: int):
    return rmodels.UserInfoDetail(
        name="john", surname="Kowalski", year_of_experience=10, position="Senior Dev", is_busy=False,
        resume_id=1
    )


@app.get("users/{user_id}/resume/{resume_id}")
def get_user_resume():
    return "Mambo Jambo"
