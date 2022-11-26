
import spacy
import os
import random

from typing import Dict
from dataclasses import dataclass
from spacy.tokens import DocBin
from spacy.training.example import Example
from parsers.ner_parser import load_and_preprocess
from nlp import DIR_PATH
from nlp.tools import split_data
from tqdm import tqdm


@dataclass
class NERScore:
    ents_p: float
    ents_r: float
    ents_f: float
    ents_per_type: Dict[str, Dict[str, float]]

    def __eq__(self, other: object):
        """
        This has to be overriden because we want to optimize using f-score value.
        """
        return self.ents_f == other.ents_f


class NER:
    
    def _load_spacy_model(self):
        # TODO - allow settings those model in settings
        if os.path.isfile(f"{DIR_PATH}/models/current_model"):
            return spacy.load(f"{DIR_PATH}/models/current_model")
        else:
            return spacy.load("en_core_web_sm")

    def __init__(self) -> None:
        # first load the proper model
        self.nlp = self._load_spacy_model()
        self.db = DocBin
        # TODO - fix this (filename)
        data = load_and_preprocess("all.jsonl")
        self._train_dataset, self._test_dataset = split_data(data)
        self.other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
        self.ner_pipe = self.nlp.get_pipe("ner")
        self.initial_score = self.evaluate_model()["ents_f"]
        # self.score = self.evaluate_model()

    def train(self, n_iter: int = 5) -> None:
        # First add entities to NER model
        data = self._train_dataset
        for _, annotations in data:
            for ent in annotations.get("entities"):
                self.ner_pipe.add_label(ent[2])
        random.shuffle(data)
        with self.nlp.disable_pipes(*self.other_pipes):
            losses = {}
            for _ in range(n_iter):
                for batch in spacy.util.minibatch(data, size=2):
                    for text, annotations in batch:
                        doc = self.nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        losses = self.nlp.update(
                            [example], losses=losses, drop=0.2
                        )
                print(losses)

    def evaluate_model(self):
        """
        Returning score for our model
        """
        examples = []
        scorer = spacy.scorer.Scorer()

        for batch in spacy.util.minibatch(self._test_dataset, size=2):
            for text, annotations in batch:
                # create Example
                doc = self.nlp(text)
                example = Example.from_dict(doc, annotations)
                example.predicted = self.nlp(doc.text)
        
            examples.append(example)
        return NERScore(**scorer.score_spans(examples, "ents"))
    
    def save_model(self):
        if self.initial_score < self.evaluate_model():
            self.nlp.to_disk(f"{DIR_PATH}/models/best_model")
        self.nlp.to_disk(f"{DIR_PATH}/models/current_model")

    def predict(self, text):
        doc = self.nlp(text)
        return self.nlp(doc.text)
