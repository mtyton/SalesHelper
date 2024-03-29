# This module contains NER data parsers
import json
import re
import pandas as pd
from typing import (
    List, 
    Dict,
    Tuple
)

from parsers.settings import PARSABLE_DATA_DIR


NER_DATA = List[Tuple[str, Dict[str, List[Tuple[int, int, str]]]]]
ALLOWED_ENT_LABELS = ['Skill', 'Position', 'Experience', 'Education']


def __preprocess_data(data: pd.Series) -> pd.Series:
    parsed_entities = []
    text = data["text"]
    invalid_span_tokens = re.compile(r'\s')

    for ent in data["entities"]:
        start, end, label = ent
        label = label.title()
        if label not in ALLOWED_ENT_LABELS:
            raise ValueError(f"Not allowed entity label: {label}")
        if start < 0:
            start = 0
        if end > len(text):
            end = len(text)
        valid_start = start
        valid_end = end
        while valid_start < len(text) and invalid_span_tokens.match(
                text[valid_start]):
            valid_start += 1
        while valid_end > 1 and invalid_span_tokens.match(
                text[valid_end - 1]):
            valid_end -= 1
        parsed_entities.append((valid_start, valid_end, label))
    return pd.Series({"text": text, "entities": parsed_entities})

def _remove_overlaping_ents(entities: NER_DATA) -> NER_DATA:
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
    data = []
    with open(f"{PARSABLE_DATA_DIR}/{filename}") as f:
        for line in f.readlines():
            line = json.loads(line)
            data.append({
                    "text": line["text"],
                    "entities": line["entities"]
            })
    df = pd.DataFrame(columns=["text", "entities"], data=data)
    df = df.apply(__preprocess_data, axis=1)
    return _dataframe_to_ner_format(df)
