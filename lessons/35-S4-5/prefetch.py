import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Fusion, FusionQuery, Prefetch

from bm25 import bm25_query

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_hybrid"
text = "non metal cooking utensils"
queries = pd.read_csv("queries.csv")
dense = np.load("query_vecs.npy")[queries.index[queries["query"] == text][0]].tolist()


def search(prefetch_limit, limit, offset=0):
    return client.query_points(
        N,
        prefetch=[
            Prefetch(query=dense, using="dense", limit=prefetch_limit),
            Prefetch(query=bm25_query(text), using="bm25", limit=prefetch_limit),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        limit=limit,
        offset=offset,
        with_payload=["title"],
    ).points


for h in search(10, 5):
    print(f"{h.score:.4f} {h.payload['title'][:40]}")

for prefetch_limit, offset in [(5, 0), (5, 5), (5, 10), (20, 5)]:
    print(f"prefetch {prefetch_limit} · offset {offset} → {len(search(prefetch_limit, 5, offset))}개")
