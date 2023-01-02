import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import(
    Base,
    engine
)
from api.routers.employees import router as employee_router
from api.routers.offers import router as offer_router
from api import settings



Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(employee_router)
app.include_router(offer_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5001, log_level="info", host="0.0.0.0", reload=True)
