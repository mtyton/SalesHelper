import spacy
import spacy_fastlang  # noqa: F401 # pylint: disable=unused-import

from typing import Optional
from bs4 import BeautifulSoup


MINIMUM_LANGUAGE_SCORE = 0.7


def detect_description_language(description: str) -> Optional[str]:
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("language_detector")
    soup = BeautifulSoup(description, features="lxml")
    description = soup.get_text()
    doc = nlp(description)
    if doc._.language_score <= MINIMUM_LANGUAGE_SCORE:
        return
    if doc._.language.upper() not in ["PL", "EN"]:
        return
        
    return doc._.language.upper()
