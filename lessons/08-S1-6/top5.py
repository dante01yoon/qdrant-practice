import numpy as np
import pandas as pd
from qdrant_client import QdrantClient

queries = pd.read_csv("queries.csv")
query_vectors = np.load("query_vecs.npy")
row = queries.index[queries["query"] == "non metal cooking utensils"][0]
client = QdrantClient(url="http://localhost:6333")

top5 = client.query_points(
    collection_name="products",
    query=query_vectors[row].tolist(),
    with_payload=True,
    limit=5,
).points

for rank, pt in enumerate(top5, start=1):
    p = pt.payload
    print(f"{rank}위 | {pt.score:.4f} | {p['brand']} | {p['color']} | {p['title'][:40]}")
