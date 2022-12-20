import uvicorn
from fastapi import FastAPI
from typing import List

from api.models import (
    ResumeMatchRequest,
    ResumeMatchResponse
)


app = FastAPI()


# TODO - this will be implemented in near future
@app.post("/ml/match", response_model=List[ResumeMatchResponse])
def get_best_matches(request_data: ResumeMatchRequest):
    ...




if __name__ == "__main__":
    uvicorn.run("main:app", port=5002, log_level="info", host="0.0.0.0", reload=True)
