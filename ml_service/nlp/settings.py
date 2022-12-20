import os


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

MODEL_PATHS = {
    "BEST_MODEL": f"{DIR_PATH}/models/best_model",
    "LATEST_MODEL": f"{DIR_PATH}/models/latest_model",
}

TRAINING_DATA_FILENAME = "all.jsonl"
