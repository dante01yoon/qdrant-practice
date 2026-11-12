import time

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

products = pd.read_parquet("products.parquet")
product_vectors = np.load("product_vecs.npy")

queries = pd.read_csv("queries.csv")
query_vectors = np.load("query_vecs.npy")
row = queries.index[queries["query"] == "non metal cooking utensils"][0]
query_vector = query_vectors[row]

client = QdrantClient(url="http://localhost:6333")

if client.collection_exists(collection_name="products"):
    client.delete_collection(collection_name="products")

client.create_collection(
    collection_name="products",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

points = [
    PointStruct(
        id=i,
        vector=product_vectors[i].tolist(),
        payload={
            "product_id": row.product_id,
            "title": row.product_title,
            "brand": row.product_brand,
            "color": row.product_color,
        },
    )
    for i, row in enumerate(products.itertuples())
]

t0 = time.perf_counter()
for start in range(0, len(points), 500):
    client.upsert(
        collection_name="products",
        wait=True,
        points=points[start:start + 500],
    )
upsert_ms = (time.perf_counter() - t0) * 1000
print(f"상품 {len(points):,}개 upsert 시간: {upsert_ms:.1f}ms")

t0 = time.perf_counter()
res_no_payload = client.query_points(
    collection_name="products",
    query=query_vector.tolist(),
    with_payload=False,
    limit=3,
).points

res_with_payload = client.query_points(
    collection_name="products",
    query=query_vector.tolist(),
    with_payload=True,
    limit=3,
).points

print("with_payload=False 결과:", res_no_payload)
print("with_payload=True 결과:", res_with_payload)

client.create_collection(
    collection_name="products_no_wait",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

t0 = time.perf_counter()
for start in range(0, len(points), 500):
    client.upsert(
        collection_name="products_no_wait",
        wait=False,
        points=points[start:start + 500],
    )
print("upsert가 돌아오기까지:", round((time.perf_counter() - t0) * 1000), "ms")
print("바로 센 개수:", client.count(collection_name="products_no_wait").count)
time.sleep(2)
print("2초 뒤 센 개수:", client.count(collection_name="products_no_wait").count)
