import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

products = pd.read_parquet("products.parquet")
vecs = np.load("product_vecs.npy")
client = QdrantClient(url="http://localhost:6333")

if client.collection_exists("products_uuid"):
    client.delete_collection("products_uuid")
client.create_collection("products_uuid", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))

print("id 0 =", client.retrieve("products", ids=[0])[0].payload["title"][:40])
resorted = products.sort_values("product_id").reset_index(drop=True)
print("정렬 뒤 0번째 줄 =", resorted.loc[0, "product_title"][:40])


def point_id(product_id):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{product_id}"))


print(point_id("B08693FP1K"))
print(point_id("B08693FP1K"))

for round_no in range(2):
    for start in range(0, len(products), 500):
        batch = products.iloc[start:start + 500]
        points = [
            PointStruct(
                id=point_id(row.product_id),
                vector=vecs[i].tolist(),
                payload={"product_id": row.product_id, "title": row.product_title},
            )
            for i, row in enumerate(batch.itertuples(), start=start)
        ]
        client.upsert("products_uuid", points=points)
    print(f"{round_no + 1}번째 넣은 뒤 개수:", client.count("products_uuid").count)
