import numpy as np
import json
from bs4 import BeautifulSoup

from database.db import conn
from parsers.settings import DIR_PATH



def load_from_db_and_preprocess() -> np.chararray:
    query = {"lang": "EN"}
    number_of_records = conn.raw_data.count_documents(query)
    data = np.chararray(number_of_records, itemsize=5000, unicode=True)
    for i, record in enumerate(conn.raw_data.find(query)):
        text_record = record["title"] +"\n"
        text_record += " ".join(record["skills"]) + "\n"
        soup = BeautifulSoup(record["description"], features="lxml")
        description_text = soup.get_text(" ")
        text_record += description_text
        data[i] = text_record
    return data


def parse_data_to_doccano_format(data):
    parsed_data = []
    for d in data:
        parsed_ents = []
        text, ents = d
        for ent in ents:
            parsed_ent = [ent.start_char, ent.end_char, ent.label_]
            parsed_ents.append(parsed_ent)
        parsed_data.append({"text": text, "label": parsed_ents})
    return parsed_data


def save_data_to_file_for_doccano_import(data):
    data = parse_data_to_doccano_format(data)
    data_json = json.dumps(data, indent=4)
    with open(f"{DIR_PATH}/doccano_export/data.jsonl", "w")  as file:
        file.writelines(data_json)
