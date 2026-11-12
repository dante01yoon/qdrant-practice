import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

products = pd.read_parquet("products.parquet")
vecs = np.load("product_vecs.npy")
client = QdrantClient(url="http://localhost:6333")


def point_id(product_id):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{product_id}"))


def make_payload(row):
    payload = {"product_id": row.product_id, "title": row.product_title}
    if isinstance(row.product_brand, str):
        payload["brand"] = row.product_brand
    if isinstance(row.product_color, str):
        payload["color"] = row.product_color.strip().lower()
    else:
        payload["color"] = None
    bullets = row.product_bullet_point.split("\n") if isinstance(row.product_bullet_point, str) else []
    payload["bullets"] = bullets
    payload["bullet_count"] = len(bullets)
    return payload


if client.collection_exists("products_payload"):
    client.delete_collection("products_payload")
client.create_collection("products_payload", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))
for start in range(0, len(products), 500):
    batch = products.iloc[start:start + 500]
    points = [PointStruct(id=point_id(r.product_id), vector=vecs[i].tolist(), payload=make_payload(r)) for i, r in enumerate(batch.itertuples(), start=start)]
    client.upsert("products_payload", points=points)

print("bullet_count:", repr(client.retrieve("products_payload", ids=[point_id("B08693FP1K")])[0].payload["bullet_count"]))

from qdrant_client.models import FieldCondition, Filter, IsEmptyCondition, IsNullCondition, PayloadField, Range

count = lambda f: client.count("products_payload", count_filter=f).count
print("brand 비어 있음:", count(Filter(must=[IsEmptyCondition(is_empty=PayloadField(key="brand"))])))
print("brand null:", count(Filter(must=[IsNullCondition(is_null=PayloadField(key="brand"))])))
print("color 비어 있음:", count(Filter(must=[IsEmptyCondition(is_empty=PayloadField(key="color"))])))
print("color null:", count(Filter(must=[IsNullCondition(is_null=PayloadField(key="color"))])))
print("특징 5개:", count(Filter(must=[FieldCondition(key="bullet_count", range=Range(gte=5))])))
print("특징 없음:", count(Filter(must=[FieldCondition(key="bullet_count", range=Range(lte=0))])))
