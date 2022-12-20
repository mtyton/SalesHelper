import argparse
import pandas as pd

from parsers.ner_parser import (
    load_and_preprocess,
    NER_DATA
)
from database.db import conn


def save_into_db(data: NER_DATA):
    for text, ents in data:
        conn.training_data.insert_one({
            "text": text,
            "ents": ents
        })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Doccano data loader",
        description="This script load data annotated in doccano.",
    )
    parser.add_argument(
        "filename", nargs="?", default="all.jsonl"
    )

    args = parser.parse_args()
    data = load_and_preprocess(args.filename)
    save_into_db(data)
