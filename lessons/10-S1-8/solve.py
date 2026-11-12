import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

products = pd.read_parquet("products.parquet")
vecs = np.load("product_vecs.npy")

raw = products["product_color"]
print("Black:", (raw == "Black").sum(), "/ black:", (raw == "black").sum(), "/ BLACK:", (raw == "BLACK").sum())


def clean(value):
    return None if pd.isna(value) else value


def norm_color(text):
    if not isinstance(text, str):
        return None
    return text.strip().lower()


none_count = 0
points = []
for i, row in enumerate(products.itertuples()):
    color = norm_color(row.product_color)
    if color is None:
        none_count += 1
    points.append(
        PointStruct(
            id=i,
            vector=vecs[i].tolist(),
            payload={
                "product_id": row.product_id,
                "title": row.product_title,
                "brand": clean(row.product_brand),
                "color": color,
            },
        )
    )

print(f"전체 {len(points):,}개 중 색상이 없는(None) 상품: {none_count:,}개")

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)


def fresh(name, distance):
    if client.collection_exists(name):
        client.delete_collection(name)
    client.create_collection(collection_name=name, vectors_config=VectorParams(size=1024, distance=distance))


def load(name):
    for start in range(0, len(points), 500):
        client.upsert(collection_name=name, wait=True, points=points[start:start + 500])


fresh("products_clean", Distance.COSINE)
load("products_clean")

queries = pd.read_csv("queries.csv")
row = queries.index[queries["query"] == "non metal cooking utensils"][0]
query_vec = np.load("query_vecs.npy")[row].tolist()
hits = client.query_points(collection_name="products_clean", query=query_vec, with_payload=True, limit=5).points
for rank, p in enumerate(hits, start=1):
    print(f"{rank}위 {p.score:.4f} | {p.payload['brand']} | {p.payload['color']} | {p.payload['title'][:30]}")

from qdrant_client.models import FieldCondition, Filter, IsEmptyCondition, MatchValue, PayloadField

black = Filter(must=[FieldCondition(key="color", match=MatchValue(value="black"))])
no_color = Filter(must=[IsEmptyCondition(is_empty=PayloadField(key="color"))])
for name, f in [("black", black), ("색상 없음", no_color)]:
    print(name, client.count(collection_name="products_clean", count_filter=f).count)
for p in client.query_points(collection_name="products_clean", query=query_vec, query_filter=black, limit=3).points:
    print(round(p.score, 4), p.payload["color"], p.payload["title"][:40])

norms = np.linalg.norm(vecs, axis=1)
print(f"상품 벡터 길이(norm) 최소: {norms.min():.1f}, 최대: {norms.max():.1f}")
fresh("products_cosine", Distance.COSINE)
fresh("products_dot", Distance.DOT)
load("products_cosine")
load("products_dot")
cos_ids = [p.id for p in client.query_points(collection_name="products_cosine", query=query_vec, limit=10).points]
dot_ids = [p.id for p in client.query_points(collection_name="products_dot", query=query_vec, limit=10).points]
print("Cosine top-10 ID:", cos_ids)
print("Dot    top-10 ID:", dot_ids)
print("순서가 완전히 같은가:", cos_ids == dot_ids)
