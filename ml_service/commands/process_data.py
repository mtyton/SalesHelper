from copy import deepcopy

from client.main import dt_client
from nlp.ner import NER


def run():
    processed_data = []
    data = dt_client.get_and_preproces_raw_data()
    ner = NER()
    # process data using NER
    for record in data:
        prediction = ner.predict(record["text"])
        entities = prediction.ents
        parsed_ents = []
        for ent in entities:
            parsed_ents.append([ent.start_char, ent.end_char, ent.label_])
        parsed_record = deepcopy(record)
        parsed_record["ents"] = parsed_ents
        processed_data.append(parsed_record)
    # send data to database for doccano export
    count = dt_client.post_doccano_data(processed_data)
    print(count)
    # TODO - add logging


if __name__ == "__main__":
    run()
