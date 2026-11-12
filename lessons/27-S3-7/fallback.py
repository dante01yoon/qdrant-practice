import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchText

client = QdrantClient(url="http://localhost:6333")
N = "products_final"
queries = pd.read_csv("queries.csv")
query_vec = np.load("query_vecs.npy")[queries.index[queries["query"] == "non metal cooking utensils"][0]].tolist()


def find(query_filter, limit):
    return client.query_points(N, query=query_vec, using="all", query_filter=query_filter, limit=limit,
                               score_threshold=0.5, with_payload=["title", "brand"]).points


def search(brand, want=3):
    same = FieldCondition(key="brand", match=MatchText(text=brand))
    hits = find(Filter(must=[same]), 10)
    print(f"[{brand}] 브랜드 안에서 {len(hits)}개")
    if len(hits) < want:
        more = find(Filter(must_not=[same]), want - len(hits))
        print(f"  → 다른 브랜드에서 {len(more)}개 채움")
        hits += more
    for h in hits:
        print(f"  {h.score:.3f} {h.payload.get('brand', '-'):16} {h.payload['title'][:36]}")


search("oxo")
search("Nike")
