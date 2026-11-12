import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

products = pd.read_parquet("products.parquet").fillna("")
title_vecs = np.load("title_vecs.npy")
detail_vecs = np.load("detail_vecs.npy")
client = QdrantClient(url="http://localhost:6333")

if client.collection_exists("products_named"):
    client.delete_collection("products_named")
client.create_collection(
    "products_named",
    vectors_config={
        "title": VectorParams(size=1024, distance=Distance.COSINE),
        "detail": VectorParams(size=1024, distance=Distance.COSINE),
    },
)

for start in range(0, len(products), 500):
    points = []
    for i, row in enumerate(products.iloc[start:start + 500].itertuples(), start=start):
        vectors = {"title": title_vecs[i].tolist()}
        if row.product_bullet_point:
            vectors["detail"] = detail_vecs[i].tolist()
        pid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{row.product_id}"))
        points.append(PointStruct(id=pid, vector=vectors, payload={"product_id": row.product_id, "title": row.product_title}))
    client.upsert("products_named", points=points)
print("개수:", client.count("products_named").count)
