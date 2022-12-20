import logging
import os


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def initializeLogger(
    logger_name: str, filename=None, logger_level=logging.DEBUG,
    file_logging_level=logging.DEBUG
):
    logger = logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)
    
    if filename:
        file_handler = logging.FileHandler(f"{DIR_PATH}/{filename}")
        file_handler.setLevel(file_logging_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
    return logger

# default logger for this package
default_logger = initializeLogger("mlDebugLogger", filename="ml.log")

training_logger = initializeLogger(
    "nerTrainingLogger", filename="traingHistory.log", 
    file_logging_level=logging.INFO, logger_level=logging.INFO
)
evaluate_logger = initializeLogger(
    "nerEvalLogger", filename="evalLogs.log", 
    file_logging_level=logging.INFO, logger_level=logging.INFO
)


MODEL_PATHS = {
    "BEST_MODEL": f"{DIR_PATH}/nlp/models/best_model",
    "LATEST_MODEL": f"{DIR_PATH}/nlp/models/latest_model",
}
