from typing import (
    Tuple,
    List, 
    Union,
    Iterator
)
import json
from dataclasses import asdict

from api.models import ResumeMatchResponse
from nlp.ner import NER
from client.main import dt_client


KNOWN_ENTITY_TYPES = ['Skill', 'Position', 'Experience', 'Education']
PARSED_ENTITY_TYPE = List[Tuple[str, str]]


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
        
    def _get_skills_matching(self, resume_entities, job_offer_entities):
        resume_skill_entities = self._filter_entities(resume_entities, desired_enttity_types=["Skill"])
        offer_skill_entities = self._filter_entities(job_offer_entities, desired_enttity_types=["Skill"])
        resume_skill_entities = [skill[0] for skill in resume_skill_entities]
        offer_skill_entities = [skill[0] for skill in offer_skill_entities]
        number_of_matched_ents = 0
        matched_skills = []
        for skill in offer_skill_entities:
            if skill in resume_skill_entities:
                matched_skills.append(skill)
                number_of_matched_ents += 1
        denominator = len(offer_skill_entities)
        ratio = float(number_of_matched_ents/denominator) if denominator else 0
        return matched_skills, ratio


    def get_single_offer_matching(self, resume, offer) -> ResumeMatchResponse:
        resume_ents = self._extract_entities(resume)
        offer_ents = self._extract_entities(offer["text"])
        _, match_ratio = self._get_skills_matching(resume_ents, offer_ents)
        return ResumeMatchResponse(offer_uuid=offer["uuid"], match_ratio=match_ratio)
