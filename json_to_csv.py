import pandas as pd
import json


def json_to_dataframe(json_file):
    with open(json_file, 'r', encoding= 'utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame([data])
    return pd.DataFrame(data)


json_file = "G1_2020.json"
df = json_to_dataframe(json_file)

df.to_csv("response.G1_2020.11.csv", index=False)
print("Done")