from typing import (
    Tuple,
    List, 
    Union
)
from dataclasses import dataclass

from nlp.ner import NER
from client.main import dt_client


KNOWN_ENTITY_TYPES = ['Skill', 'Position', 'Experience', 'Education']
PARSED_ENTITY_TYPE = List[Tuple(str, str)]


@dataclass
class Match:
    ...


class Matcher:

    def __init__(self) -> None:
        self.ner = NER()

    def _filter_entities(
        self, entities: PARSED_ENTITY_TYPE, desired_enttity_types: Union[List[str], str]
    ) -> PARSED_ENTITY_TYPE:
        """
        This method should returned entities filtered by type
        """
        if isinstance(desired_enttity_types, str):
            desired_enttity_types = [desired_enttity_types]

        if not all(s in KNOWN_ENTITY_TYPES for s in desired_enttity_types):
            raise ValueError(
                "Unnkown type of entity, it is impossible to filter."
            )
        parsed_entities = []
        for entity in entities:
            _, label = entity
            if label not in desired_enttity_types:
                continue
            parsed_entities.append(entity)
        return parsed_entities

    def _extract_entities(self, text: str) -> PARSED_ENTITY_TYPE:
        document = self.ner.predict(text)
        return [(ent.text, ent.label_) for ent in document.ents]
        
    def _get_skills_matching(self, text_entities, job_offer_entities):
        ...

    def _get_single_offer_matching(self, resume, offer):
        entities_matching_rate = self._get_entities_matching()

    def get_best_matches(self, resume):
        offers = dt_client.get_filtered_raw_data(number_of_records=20)
        matches = []
        for offer in offers:
            ...
        

