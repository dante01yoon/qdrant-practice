import time

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, Range, SearchParams

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, timeout=60)
N = "products_100k"
query_vecs = np.load("query_vecs.npy")[:200]


def measure(query_filter, ef=None):
    recall, times = [], []
    for q in query_vecs:
        exact = {p.id for p in client.query_points(N, query=q.tolist(), query_filter=query_filter, limit=10,
                                                   search_params=SearchParams(exact=True)).points}
        t0 = time.perf_counter()
        got = {p.id for p in client.query_points(N, query=q.tolist(), query_filter=query_filter, limit=10,
                                                 search_params=SearchParams(hnsw_ef=ef)).points}
        times.append((time.perf_counter() - t0) * 1000)
        recall.append(len(got & exact) / 10)
    return np.mean(recall), np.median(times)


def keep(per_mille):
    return Filter(must=[FieldCondition(key="bucket", range=Range(lt=per_mille))])


def show(label, result):
    print(f"{label:14} recall {result[0]:.3f} · {result[1]:.2f}ms")


if __name__ == "__main__":
    show("필터 없음", measure(None))
    for per_mille in [500, 100, 10, 1]:
        show(f"필터 {per_mille / 10:g}%", measure(keep(per_mille)))
    for ef in [256, 512]:
        show(f"필터 50% ef={ef}", measure(keep(500), ef))
