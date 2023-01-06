import uvicorn
import json
from dataclasses import asdict
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import List
from uuid import UUID
from bson.binary import Binary


from database.db import conn
from database.models import (
    DoccanoDataDocument,
    TrainingDataDocument,
    JobOfferDocument
)
from database.schemas import (
    JobOffer,
    DoccanoData,
    OfferCategories
)
from parsers.mongodb_data_parser import parse_data_to_doccano_format


app = FastAPI()


@app.get("/data/training")
def get_training_data():
    document = TrainingDataDocument()
    data = document.find({})
    return [(r.text, r.ents) for r in data]


@app.post("/data/doccano", status_code=201)
def save_doccano_data(data: List[DoccanoData]):
    counter = 0
    document = DoccanoDataDocument()
    for d in data:
        row_data = asdict(d)
        document.insert(**row_data)
        counter += 1
    return {"inserted": counter}


@app.get("/data/doccano-export")
def export_doccano_data():
    document = DoccanoDataDocument()
    def generate_data():
        data = parse_data_to_doccano_format(((elem.text, elem.ents) for elem in document.find({})))
        for d in data:
            yield f"{json.dumps(d)}\n"
    return StreamingResponse(generate_data(), media_type="jsonl")
    

# NOTE returns raw data only for being tagged - not to use as offer list!!!
@app.get("/data/raw", response_model=List[JobOffer])
def get_raw_data():
    document = JobOfferDocument()
    query = {"lang": "EN"} 
    return document.find(query)


@app.get("/data/offers", response_model=List[JobOffer])
def get_job_offers(skip: int = 0, limit: int = 25, category_name: str = None):
    document = JobOfferDocument()
    query = {"lang": "EN"}
    if category_name is not None:
        category = OfferCategories.from_text(category_name)
        query["category"] = category
    queryset = document.find(query, skip=skip, limit=limit)
    return queryset


@app.get("/data/offers/{offer_uuid}", response_model=JobOffer)
def get_job_offer(offer_uuid: UUID):
    document = JobOfferDocument()
    query = {"uuid": Binary.from_uuid(offer_uuid)}
    return document.find(query, find_one=True)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", host="0.0.0.0", reload=True)
