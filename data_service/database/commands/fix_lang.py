from tools import detect_description_language

from database.db import conn


if __name__ == "__main__":
    elems = []
    for elem in conn.raw_data.find({}):
        lang = detect_description_language(elem["description"])
        if not lang:
            conn.raw_data.delete_one({"_id": elem["_id"]})
            print(elem["description"])
            continue
        elems.append(elem)


    for elem in elems:
        result = conn.raw_data.update_one({"_id": elem["_id"]}, {"$set": {"lang": lang}})
    print(f"Result: {result}")