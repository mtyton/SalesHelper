from typing import (
    Optional,
    Tuple,
    Dict
)
import spacy
import spacy_fastlang

from parsers.ner_parser import NER_DATA


MINIMUM_LANGUAGE_SCORE = 0.7


def detect_description_language(description: str) -> Optional[str]:
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("language_detector")
    doc = nlp(description)
    if doc._.language_score <= MINIMUM_LANGUAGE_SCORE:
        return
    return doc._.language.upper()
 

def split_data(data: NER_DATA, split_ratio: float = 0.8) -> Tuple[NER_DATA, NER_DATA]:
    number_of_data = len(data)
    split_point = int(number_of_data * split_ratio)
    return data[:split_point], data[split_point:]


def verify_missaligned_ents(data):
    ...
