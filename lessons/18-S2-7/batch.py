import time
import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

products = pd.read_parquet("products.parquet").fillna("")
vecs = np.load("product_vecs.npy")
client = QdrantClient(url="http://localhost:6333")

ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{p}")) for p in products["product_id"]]
points = [PointStruct(id=ids[i], vector=vecs[i].tolist(), payload={"title": t}) for i, t in enumerate(products["product_title"])]


def fresh():
    if client.collection_exists("products_batch"):
        client.delete_collection("products_batch")
    client.create_collection("products_batch", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))


def load(size):
    fresh()
    t0 = time.perf_counter()
    for start in range(0, len(points), size):
        client.upsert("products_batch", points=points[start:start + size])
    return time.perf_counter() - t0


for size in [16, 64, 256, 500, 1000]:
    print(f"{size:>5}개씩: {load(size):.1f}초")
