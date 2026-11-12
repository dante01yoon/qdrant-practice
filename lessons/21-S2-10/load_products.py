import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

NAME = "products_final"
VECTORS = {"all": "product_vecs.npy", "title": "title_vecs.npy", "detail": "detail_vecs.npy"}


def point_id(product_id):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{product_id}"))


def make_payload(row):
    payload = {"product_id": row.product_id, "title": row.product_title}
    if isinstance(row.product_brand, str):
        payload["brand"] = row.product_brand
    payload["color"] = row.product_color.strip().lower() if isinstance(row.product_color, str) else None
    bullets = row.product_bullet_point.split("\n") if isinstance(row.product_bullet_point, str) else []
    payload["bullets"] = bullets
    payload["bullet_count"] = len(bullets)
    payload["has_description"] = isinstance(row.product_description, str)
    return payload


def make_points(products, vecs):
    for i, row in enumerate(products.itertuples()):
        vectors = {"all": vecs["all"][i].tolist(), "title": vecs["title"][i].tolist()}
        if isinstance(row.product_bullet_point, str):
            vectors["detail"] = vecs["detail"][i].tolist()
        yield PointStruct(id=point_id(row.product_id), vector=vectors, payload=make_payload(row))


def main():
    products = pd.read_parquet("products.parquet")
    vecs = {name: np.load(path) for name, path in VECTORS.items()}
    client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
    if not client.collection_exists(NAME):
        client.create_collection(NAME, vectors_config={name: VectorParams(size=1024, distance=Distance.COSINE) for name in VECTORS})
    client.upload_points(NAME, points=make_points(products, vecs), batch_size=256, wait=True)
    print("개수:", client.count(NAME).count)
    p = client.retrieve(NAME, ids=[point_id("B08693FP1K")])[0].payload
    print({k: (v[:20] if isinstance(v, str) else v) for k, v in p.items() if k != "bullets"}, "특징", len(p["bullets"]), "줄")


if __name__ == "__main__":
    main()
