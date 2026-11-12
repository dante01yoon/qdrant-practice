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
for start in range(0, len(points), 500):
    client.upsert(
        collection_name="products",
        wait=True,
        points=points[start:start + 500],
    )
