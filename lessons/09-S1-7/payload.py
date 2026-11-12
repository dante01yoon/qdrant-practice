import time
import numpy as np
import pandas as pd
from qdrant_client import QdrantClient

queries = pd.read_csv("queries.csv")
row = queries.index[queries["query"] == "non metal cooking utensils"][0]
query_vec = np.load("query_vecs.npy")[row].tolist()
rest_client = QdrantClient(url="http://localhost:6333")


def bench_payload(payload_opt, runs=100):
    rest_client.query_points(collection_name="products", query=query_vec, limit=5, with_payload=payload_opt)
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        rest_client.query_points(collection_name="products", query=query_vec, limit=5, with_payload=payload_opt)
        times.append((time.perf_counter() - t0) * 1000)
    return np.median(times)


full_med = bench_payload(True)
part_med = bench_payload(["title", "brand"])
print(f"전체 payload 중앙값: {full_med:.2f}ms")
print(f"상품명·브랜드만 중앙값: {part_med:.2f}ms")
