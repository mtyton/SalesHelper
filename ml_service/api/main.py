import uvicorn
import json
import typing
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import Iterator
from dataclasses import asdict

from api.models import (
    ResumeMatchRequest,
    ResumeMatchResponse
)
from match.matchers import Matcher
from client.main import dt_client


app = FastAPI()

matcher = Matcher()


@app.post("/ml/match", status_code=200)
async def get_best_matches(request_data: ResumeMatchRequest, category: str):
    offers = dt_client.get_filtered_raw_data(category_name=category)
    async def get_best_matches(
        resume
    ) -> Iterator[ResumeMatchResponse]:
        for offer in offers:
            match = matcher.get_single_offer_matching(resume, offer)
            yield json.dumps(asdict(match))

    return StreamingResponse(
       get_best_matches(request_data.resume) , status_code=200, media_type="app/json",
    )


async def fake_video_streamer():
    for i in range(2048):
        yield f"{i}"


@app.get("/video")
async def main():
    return StreamingResponse(fake_video_streamer())


if __name__ == "__main__":
    uvicorn.run("main:app", port=5002, log_level="info", host="0.0.0.0", reload=True)
