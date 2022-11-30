from parsers.mongodb_data_parser import (
    load_from_db_and_preprocess,
    save_data_to_file_for_doccano_import
)
from nlp.ner import NER


def run():
    data = load_from_db_and_preprocess()
    ner = NER()
    ner_processed_data = []
    for d in data:
        text = d
        prediction = ner.predict(d)
        entities = prediction.ents
        ner_processed_data.append((text, entities))
    save_data_to_file_for_doccano_import(ner_processed_data)


if __name__ == "__main__":
    run()
