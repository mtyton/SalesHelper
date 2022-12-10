import uvicorn
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import List
from bson.binary import Binary


from database.db import conn
from api.models import (
    RawEntryResponseModel,
    NlpProcessedData,
    DoccanoAnnotatedData
)
from parsers.mongodb_data_parser import parse_data_to_doccano_format


app = FastAPI()


@app.get("/data/training")
def get_training_data():
    data = conn.training_data.find()
    return [(r["text"], r["ents"]) for r in data]


@app.post("/data/doccano", status_code=201)
def save_doccano_data(data: List[NlpProcessedData]):
    counter = 0
    for d in data:
        existing_entry = conn.doccano_data.find_one({"uuid":  Binary.from_uuid(d.uuid)})
        if not existing_entry:
            row_data = d.dict()
            row_data["uuid"] = Binary.from_uuid(row_data["uuid"])
            conn.doccano_data.insert_one(row_data)
            counter += 1
    return {"inserted": counter}


@app.get("/data/doccano-export")
def export_doccano_data():
    def generate_data():
        data = parse_data_to_doccano_format(((elem["text"], elem["ents"]) for elem in conn.doccano_data.find()))
        for d in data:
            yield f"{json.dumps(d)}\n"
    return StreamingResponse(generate_data(), media_type="jsonl")
    

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
