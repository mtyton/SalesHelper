from typing import List
from sqlalchemy.orm import Session

from fastapi import (
    FastAPI,
    Depends
)
from api import models as rmodels
from database import models as db_models
from database.db import (
    get_db, 
    Base,
    engine
)


Base.metadata.create_all(bind=engine)

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
def get_users_list(db: Session = Depends(get_db)):
    data = db.query(db_models.Employee).offset(0).limit(10).all()

    return [rmodels.UserInfo.from_db_instance(d) for d in data]


@app.post("/users", response_model=rmodels.UserInfo)
def create_user(user_data: rmodels.UserInfoCreateRequest, db: Session = Depends(get_db)):
    db_instance = user_data.save_to_db(db)
    return rmodels.UserInfo.from_db_instance(db_instance)


@app.get("/users/{user_id}", response_model=rmodels.UserInfoDetail)
def get_user_details(user_id: int):
    db = get_db()
    db_user = db.query(db_models.Employee).filter(user_id=user_id).first()
    return rmodels.UserInfoDetail.from_db_instance(db_user)


@app.get("users/{user_id}/resume/", response_model=rmodels.ResumeResponse)
def get_user_resume(user_id: int, db: Session = Depends(get_db)):
    resume = db.query(db_models.Resume).filter(owner_id=user_id).first()
    return rmodels.ResumeResponse.from_db_instance(resume)


@app.post("users/{user_id}/resume", response_model=rmodels.ResumeResponse)
def create_user_resume(user_id:int, resume: rmodels.ResumeCreateRequest, db: Session = Depends(get_db)):
    resume = db.query(db_models.Resume).filter(owner_id=user_id).first()
    if not resume:
        resume = rmodels.ResumeCreateRequest.save_to_db(db)
    return rmodels.ResumeResponse.from_db_instnace(resume)
