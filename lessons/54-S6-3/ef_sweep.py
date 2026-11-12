import time

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import CollectionStatus, Distance, SearchParams, VectorParams

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, timeout=600)
vecs = np.load("vecs_100k.npy", mmap_mode="r")
queries = np.load("query_vecs.npy")[:200]
N = "hnsw_test"


if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=VectorParams(size=1024, distance=Distance.COSINE))
client.upload_collection(N, vectors=vecs, ids=range(len(vecs)), batch_size=500, wait=True)
while (info := client.get_collection(N)).status != CollectionStatus.GREEN or info.indexed_vectors_count < 0.9 * len(vecs):
    time.sleep(0.5)


def run(params):
    got, ms = [], []
    for q in queries:
        t0 = time.perf_counter()
        got.append({p.id for p in client.query_points(N, query=q.tolist(), limit=10, search_params=params).points})
        ms.append((time.perf_counter() - t0) * 1000)
    return got, np.median(ms)


truth, exact_ms = run(SearchParams(exact=True))
print(f"exact        · 정답 · {exact_ms:.1f}ms")
for ef in [16, 32, 64, 128, 256]:
    got, ms = run(SearchParams(hnsw_ef=ef))
    print(f"hnsw_ef {ef:3}  · recall@10 {np.mean([len(g & t) / 10 for g, t in zip(got, truth)]):.3f} · {ms:.1f}ms")
