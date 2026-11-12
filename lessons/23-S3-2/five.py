import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchExcept, MatchValue, Range, ValuesCount

client = QdrantClient(url="http://localhost:6333")
N = "products_final"
count = lambda f: client.count(N, count_filter=f).count

rule = Filter(must=[
    FieldCondition(key="bullet_count", match=MatchValue(value=5)),
    FieldCondition(key="color", match=MatchExcept(**{"except": ["black", "white"]})),
])
print("특징 5개 · 색상 있음 · 검정·흰색 아님:", count(rule))

queries = pd.read_csv("queries.csv")
q = np.load("query_vecs.npy")[queries.index[queries["query"] == "non metal cooking utensils"][0]]
for h in client.query_points(N, query=q.tolist(), using="all", query_filter=rule, limit=3, with_payload=["title", "color", "bullet_count"]).points:
    print(f"  {h.score:.3f} {h.payload['color']:12} {h.payload['bullet_count']} {h.payload['title'][:50]}")

print("\n특징 5개 이상(gte):", count(Filter(must=[FieldCondition(key="bullet_count", range=Range(gte=5))])),
      "/ 5개 초과(gt):", count(Filter(must=[FieldCondition(key="bullet_count", range=Range(gt=5))])))
print("목록 길이로(values_count gte 5):", count(Filter(must=[FieldCondition(key="bullets", values_count=ValuesCount(gte=5))])))
