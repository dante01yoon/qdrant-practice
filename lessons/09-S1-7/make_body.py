import json
import numpy as np
import pandas as pd

queries = pd.read_csv("queries.csv")
row = queries.index[queries["query"] == "non metal cooking utensils"][0]
query_vec = np.load("query_vecs.npy")[row].tolist()

body = {
    "query": query_vec,
    "limit": 3,
    "with_payload": ["title", "brand"],
}

with open("query_body.json", "w", encoding="utf-8") as f:
    json.dump(body, f)

print("요청 JSON 파일 크기:", len(json.dumps(body).encode("utf-8")), "바이트")
