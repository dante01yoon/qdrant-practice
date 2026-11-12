import time
import numpy as np
import pandas as pd
from qdrant_client import QdrantClient

queries = pd.read_csv("queries.csv")
row = queries.index[queries["query"] == "non metal cooking utensils"][0]
query_vec = np.load("query_vecs.npy")[row].tolist()

rest_client = QdrantClient(url="http://localhost:6333")
grpc_client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)


def measure(client, runs=100):
    client.query_points(collection_name="products", query=query_vec, limit=5, with_payload=True)
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        client.query_points(collection_name="products", query=query_vec, limit=5, with_payload=True)
        times.append((time.perf_counter() - t0) * 1000)
    return np.median(times), np.percentile(times, 95)


rest_med, rest_p95 = measure(rest_client)
grpc_med, grpc_p95 = measure(grpc_client)
print(f"REST -> 중앙값: {rest_med:.2f}ms, p95: {rest_p95:.2f}ms")
print(f"gRPC -> 중앙값: {grpc_med:.2f}ms, p95: {grpc_p95:.2f}ms")
