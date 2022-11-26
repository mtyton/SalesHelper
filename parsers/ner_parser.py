# This module contains NER data parsers
import json
import pandas as pd
from typing import (
    List, 
    Dict,
    Tuple
)

from parsers import DIR_PATH


NER_DATA = List[Tuple[str, Dict[str, List[Tuple[int, int, str]]]]]


def __preprocess_data(data: pd.Series) -> pd.Series:
    parsed_entities = []
    text = data["text"]
    for ent in data["entities"]:
        start, end, label = ent
        # TODO check if start, and end are in the text
        while text[start+1] == "\s":
            start += 1
        while text[end-1] == "\s":
            end -= 1
        parsed_entities.append((start, end, label))
    return pd.Series({"text": text, "entities": parsed_entities})

# TODO - remove overlaping entities
def _remove_overlaping_ents(entities: NER_DATA) -> NER_DATA:
    parsed_entities = []
    for x, ent1 in enumerate(entities):
        ent1_start, ent1_end, _ = ent1
        copied_entities = entities[:x] + entities[x+1:]
        for ent2 in copied_entities:
            ent2_start, ent2_end, _ = ent2
            if (
                (ent2_start >= ent1_start and ent2_start <= ent1_end) or
                (ent2_end <= ent1_end and ent2_end >= ent1_start)
            ):
                ent1_len = ent1_end - ent1_start
                ent2_len = ent2_end - ent2_start
                ent = ent1 if ent1_len < ent2_len else ent2
                entities.remove(ent)

    return entities

def _parse_entities(entities: List[Dict]) -> Tuple[str, int, int]:
    parsed_entities = []
    for ent in entities:
        parsed_entities.append((
            ent["start_offset"], 
            ent["end_offset"], 
            ent["label"]
        ))
    return _remove_overlaping_ents(parsed_entities)

def _dataframe_to_ner_format(df) -> NER_DATA:
    data = []
    for i in range(df.shape[0]):
        row = df.iloc[i]
        data.append((
            row["text"],
            {"entities": row["entities"]}
        ))
    return data

def load_and_preprocess(filename: str) -> NER_DATA:
    df = pd.DataFrame(columns=["text", "entities"])
    with open(f"{DIR_PATH}/parsable_data/{filename}") as f:
        for line in f.readlines():
            line = json.loads(line)
            line_data = pd.DataFrame({
                "text": line["text"],
                "entities": [_parse_entities(line["entities"])]
            })
            df = pd.concat([df, line_data], ignore_index=True)
    df = df.apply(__preprocess_data, axis=1)
    return _dataframe_to_ner_format(df)
