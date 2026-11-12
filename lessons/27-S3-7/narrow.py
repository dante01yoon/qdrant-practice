import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

client = QdrantClient(url="http://localhost:6333")
N = "products_final"
queries = pd.read_csv("queries.csv")
query_vec = np.load("query_vecs.npy")[queries.index[queries["query"] == "non metal cooking utensils"][0]].tolist()


def search(brand, threshold=None):
    f = Filter(must=[FieldCondition(key="brand", match=MatchValue(value=brand))])
    hits = client.query_points(N, query=query_vec, using="all", query_filter=f, limit=10,
                               score_threshold=threshold, with_payload=["title"]).points
    print(f"[{brand}] {len(hits)}개")
    for h in hits:
        print(f"  {h.score:.3f} {h.payload['title'][:32]}")
    return hits


search("OXO")
search("OXO", threshold=0.5)


def safe_search(brand):
    hits = search(brand, threshold=0.5)
    if not hits:
        print("  → 조건에 맞는 상품이 없어요. 브랜드 철자를 확인하거나 브랜드 없이 찾아볼게요.")
    return hits


safe_search("Nike")
