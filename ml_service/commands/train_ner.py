import argparse

from nlp.ner import NER


if __name__ == "__main__":
    ner = NER()
    ner.train()
