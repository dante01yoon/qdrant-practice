import sys
import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

products = pd.read_parquet("products.parquet").fillna("")
vecs = np.load("product_vecs.npy")
client = QdrantClient(url="http://localhost:6333")


def point_id(product_id):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{product_id}"))


STOP = int(sys.argv[1]) if len(sys.argv) > 1 else None

if not client.collection_exists("products_load"):
    client.create_collection("products_load", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))

try:
    for k, start in enumerate(range(0, len(products), 500)):
        if k == STOP:
            raise RuntimeError("연습: 적재 중간에 끊김")
        batch = products.iloc[start:start + 500]
        points = [
            PointStruct(id=point_id(r.product_id), vector=vecs[i].tolist(),
                        payload={"product_id": r.product_id, "title": r.product_title, "brand": r.product_brand})
            for i, r in enumerate(batch.itertuples(), start=start)
        ]
        client.upsert("products_load", points=points)
finally:
    print("지금 개수:", client.count("products_load").count)
