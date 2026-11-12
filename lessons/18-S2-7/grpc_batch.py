import time
import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

products = pd.read_parquet("products.parquet")
vecs = np.load("product_vecs.npy")
client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
points = [PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{p}")), vector=vecs[i].tolist(), payload={"title": t})
          for i, (p, t) in enumerate(zip(products["product_id"], products["product_title"]))]


def fresh():
    if client.collection_exists("products_batch"):
        client.delete_collection("products_batch")
    client.create_collection("products_batch", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))


for size in [64, 256, 1024, 4096, len(points)]:
    fresh()
    t0 = time.perf_counter()
    try:
        for start in range(0, len(points), size):
            client.upsert("products_batch", points=points[start:start + size])
        print(f"gRPC {size:>5}개씩: {time.perf_counter() - t0:.1f}초 · 개수 {client.count('products_batch').count}")
    except Exception as e:
        print(f"gRPC {size:>5}개씩: 실패 · {str(e)[:160]}")
