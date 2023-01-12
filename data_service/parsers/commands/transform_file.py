import pandas as pd
import json

from parsers.settings import PARSABLE_DATA_DIR


if __name__ == "__main__":
    data = []
    with open(f"{PARSABLE_DATA_DIR}/new_admin.jsonl") as f:
        for line in f.readlines():
            line = json.loads(line)
            data.append({
                    "text": line["text"],
                    "entities": line["label"]
            })
    df = pd.DataFrame(columns=["text", "entities"], data=data)
    print(df.head(2))
    with open(f"{PARSABLE_DATA_DIR}/new_admin_parsed.jsonl", "w") as f:
        for i, row in df.iterrows():
            f.write(row.to_json()+"\n")
