from typing import Optional
import spacy
import spacy_fastlang


MINIMUM_LANGUAGE_SCORE = 0.7


def detect_description_language(description: str) -> Optional[str]:
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("language_detector")
    doc = nlp(description)
    if doc._.language_score <= MINIMUM_LANGUAGE_SCORE:
        return
    return doc._.language.upper()
