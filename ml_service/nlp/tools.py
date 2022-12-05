from typing import (
    List,
    Tuple,
    Dict
)
import spacy
import spacy_fastlang

# TODO - add this typing
# from parsers.ner_parser import NER_DATA


NER_DATA = List[Tuple[str, Dict[str, List[Tuple[int, int, str]]]]] 


def split_data(data: NER_DATA, split_ratio: float = 0.8) -> Tuple[NER_DATA, NER_DATA]:
    number_of_data = len(data)
    split_point = int(number_of_data * split_ratio)
    return data[:split_point], data[split_point:]


def verify_missaligned_ents(data):
    ...
