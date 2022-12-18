
import spacy
import os
import random
import datetime
import json

from typing import Dict
from dataclasses import (
    dataclass, 
    asdict
)
from spacy.tokens import DocBin
from spacy.training.example import Example
from settings import (
    MODEL_PATHS,
    training_logger,
    evaluate_logger
)
from nlp.tools import split_data
from client.main import dt_client


@dataclass
class NERScore:
    ents_p: float
    ents_r: float
    ents_f: float
    ents_per_type: Dict[str, Dict[str, float]]

    def __eq__(self, other: object):
        return self.ents_f == other.ents_f

    def __gt__(self, other: object):
        return self.ents_f > other.ents_f

    def __ge__(self, other: object):
        return self.ents_f >= other.ents_f

    def __lt__(self, other: object):
        return self.ents_f < other.ents_f

    def __le__(self, other: object):
        return self.ents_f <= other.ents_f
    

class NER:
    
    def _load_spacy_model(self, use_latest: bool=False):
        # By default we use best model not the latest model.
        if use_latest and os.path.isdir(MODEL_PATHS["LATEST_MODEL"]):
            return spacy.load(MODEL_PATHS["LATEST_MODEL"])

        if os.path.isdir(MODEL_PATHS["BEST_MODEL"]):
            return spacy.load(MODEL_PATHS["BEST_MODEL"])
        else:
            return spacy.load("en_core_web_sm")

    def __init__(self, use_latest: bool=False) -> None:
        # first load the proper model
        self.nlp = self._load_spacy_model(use_latest)
        data = dt_client.get_training_data()
        self._train_dataset, self._test_dataset = split_data(data)
        self.other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
        self.ner_pipe = self.nlp.get_pipe("ner")
        self.initial_score = self.evaluate_model(save_score=False)
        self.current_score = None

    _get_step_loss = lambda prev_losses, curr_losses: curr_losses["ner"] - prev_losses["ner"]

    def train(self, n_iter: int = 5) -> None:
        # First add entities to NER model
        training_logger.info(
            f"Training started at: {datetime.datetime.now()}, number of steps: {n_iter}"
        )
        data = self._train_dataset
        for _, annotations in data:
            for ent in annotations.get("entities"):
                self.ner_pipe.add_label(ent[2])
        random.shuffle(data)
        with self.nlp.disable_pipes(*self.other_pipes):
            prev_losses = curr_losses = {"ner": 0.0}
            for step in range(n_iter):
                for batch in spacy.util.minibatch(data, size=2):
                    for text, annotations in batch:
                        doc = self.nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        curr_losses = self.nlp.update(
                            [example], losses=curr_losses, drop=0.2
                        )
                    
                training_logger.info(
                    f"Step number: {step}, loss: {self._get_step_loss(prev_losses, curr_losses)}"
                )
                curr_losses = prev_losses
        # by the end of the training run evaluation
        self.evaluate_model()

    def evaluate_model(self, save_score=True):
        """
        Returning score for our model
        * save_score - determines if score should be save to local variable
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
        score = NERScore(**scorer.score_spans(examples, "ents"))
        if save_score:
            evaluate_logger.info(
                f"NER score: {json.dumps(asdict(score))}"
            )
            self.current_score = score
        return score

    def save_model(self):
        if not self.current_score:
            self.evaluate_model()

        if self.initial_score < self.current_score:
            self.nlp.to_disk(MODEL_PATHS["BEST_MODEL"])
        self.nlp.to_disk(MODEL_PATHS["LATEST_MODEL"])

    def predict(self, text):
        doc = self.nlp(text)
        return self.nlp(doc.text)
