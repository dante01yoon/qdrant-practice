import time

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchText, MatchValue, Range

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_final"
queries = pd.read_csv("queries.csv")
query_vec = np.load("query_vecs.npy")[queries.index[queries["query"] == "non metal cooking utensils"][0]].tolist()

FILTERS = {
    "color=black": Filter(must=[FieldCondition(key="color", match=MatchValue(value="black"))]),
    "특징 5개 이상": Filter(must=[FieldCondition(key="bullet_count", range=Range(gte=5))]),
    "상품명 spatula": Filter(must=[FieldCondition(key="title", match=MatchText(text="spatula"))]),
}


def median_ms(fn):
    times = []
    for _ in range(100):
        t0 = time.perf_counter()
        fn()
        times.append((time.perf_counter() - t0) * 1000)
    return np.median(times)


def run(tag):
    for name, f in FILTERS.items():
        count_ms = median_ms(lambda: client.count(N, count_filter=f))
        search_ms = median_ms(lambda: client.query_points(N, query=query_vec, using="all", query_filter=f, limit=10))
        print(f"{tag} | {name:10} | count {count_ms:5.2f}ms | 검색 {search_ms:5.2f}ms")


run("인덱스 있음")
for field in ["color", "bullet_count", "title", "has_description"]:
    client.delete_payload_index(N, field)
run("인덱스 없음")
