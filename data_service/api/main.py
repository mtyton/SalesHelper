import uvicorn
from fastapi import FastAPI
from typing import List
from bson.binary import Binary
from uuid import UUID

from database.db import conn
from api.models import (
    RawEntryResponseModel,
    NlpProcessedRequestData
)


app = FastAPI()

@app.get("/data/training")
def get_training_data():
    ...


@app.post("/data/doccano", status_code=201)
def save_doccano_data(data: List[NlpProcessedRequestData]):
    counter = 0
    for d in data:
        existing_entry = conn.doccano_data.find_one({"uuid":  Binary.from_uuid(d.uuid)})
        if not existing_entry:
            row_data = d.dict()
            row_data["uuid"] = Binary.from_uuid(row_data["uuid"])
            conn.doccano_data.insert_one(row_data)
            counter += 1
    return {"inserted": counter}


@app.get("/data/doccano-export", response_model=List[NlpProcessedRequestData])
def export_doccano_data():
    # TODO - return file
    return [d for d in conn.doccano_data.find()]
    

@app.get("/data/raw", response_model=List[RawEntryResponseModel])
def get_raw_data():
    # TODO - add filtering
    # TODO - add pagination
    query = {"lang": "EN"}
    queryset = conn.raw_data.find(query)
    response_data = []
    for elem in queryset:
        response_data.append(RawEntryResponseModel(**elem))
    return response_data


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", host="0.0.0.0", reload=True)
