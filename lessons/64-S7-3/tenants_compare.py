import subprocess
import time

import numpy as np
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, timeout=300)
vecs = np.load("product_vecs.npy", mmap_mode="r")
parts = np.array_split(np.arange(len(vecs)), 50)
params = models.VectorParams(size=1024, distance=models.Distance.COSINE)
disk = lambda pattern: subprocess.run(["docker", "exec", "qdrant-course", "sh", "-c", f"du -cm /qdrant/storage/collections/{pattern} | tail -1"], capture_output=True, text=True).stdout.split()[0]


def median_ms(fn):
    out = []
    for _ in range(50):
        t0 = time.perf_counter()
        fn()
        out.append((time.perf_counter() - t0) * 1000)
    return np.median(out)


t0 = time.perf_counter()
for k, ids in enumerate(parts):
    client.create_collection(f"seller_{k}", vectors_config=params)
    client.upload_collection(f"seller_{k}", vectors=vecs[ids], ids=ids.tolist(), batch_size=256, wait=True)
print(f"컬렉션 50개 · {time.perf_counter() - t0:.1f}초 · 디스크 {disk('seller_*')}MB · 검색 {median_ms(lambda: client.query_points('seller_7', query=vecs[0].tolist(), limit=10)):.1f}ms")
for k in range(50):
    client.delete_collection(f"seller_{k}")


t0 = time.perf_counter()
client.create_collection("all_sellers", vectors_config=params)
client.create_payload_index("all_sellers", "seller", field_schema=models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD, is_tenant=True))
seller = np.zeros(len(vecs), dtype=int)
for k, ids in enumerate(parts):
    seller[ids] = k
client.upload_collection("all_sellers", vectors=vecs, ids=range(len(vecs)), payload=[{"seller": int(s)} for s in seller], batch_size=256, wait=True)
only = models.Filter(must=[models.FieldCondition(key="seller", match=models.MatchValue(value=7))])
print(f"컬렉션 1개 · {time.perf_counter() - t0:.1f}초 · 디스크 {disk('all_sellers')}MB · 검색 {median_ms(lambda: client.query_points('all_sellers', query=vecs[0].tolist(), query_filter=only, limit=10)):.1f}ms")
client.delete_collection("all_sellers")
