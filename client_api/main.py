import uvicorn
from api import app


# TODO - basic auth
# TODO - maybe add registration
# TODO - add list of possible job offers
# TODO - add endpoint to sent job offer uuid and cv text in json



if __name__ == "__main__":
    uvicorn.run("main:app", port=5001, log_level="info", host="0.0.0.0", reload=True)
