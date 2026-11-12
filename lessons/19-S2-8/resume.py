import json
import os
import time
import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

products = pd.read_parquet("products.parquet").fillna("")
vecs = np.load("product_vecs.npy")
client = QdrantClient(url="http://localhost:6450", timeout=5)
CK = "checkpoint.json"


def point_id(product_id):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{product_id}"))


if not client.collection_exists("products_resume"):
    client.create_collection("products_resume", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))

next_start = json.load(open(CK))["next"] if os.path.exists(CK) else 0
print("시작 위치:", next_start)

for start in range(next_start, len(products), 500):
    batch = products.iloc[start:start + 500]
    points = [PointStruct(id=point_id(r.product_id), vector=vecs[i].tolist(), payload={"title": r.product_title})
              for i, r in enumerate(batch.itertuples(), start=start)]
    for attempt in range(1, 4):
        try:
            client.upsert("products_resume", points=points)
            break
        except Exception as e:
            print(f"  {start}번 묶음 실패 {attempt}번째: {type(e).__name__}")
            time.sleep(2 * attempt)
    else:
        raise SystemExit(f"세 번 실패 · {start}번 묶음에서 멈춤")
    json.dump({"next": start + 500}, open(CK, "w"))
    print(f"{start + len(batch):>6}개까지 넣음")

print("끝 · 개수:", client.count("products_resume").count)
