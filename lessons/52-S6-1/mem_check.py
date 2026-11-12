import subprocess
import time

import numpy as np
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import CollectionStatus, Distance, VectorParams

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, timeout=600)
vecs = np.load("vecs_100k.npy", mmap_mode="r")
N = "mem_test"
MB = 1024 * 1024


n, dim, m = len(vecs), 1024, 16
print(f"공식 · 벡터 {n * dim * 4 / MB:.0f}MB · HNSW {n * m * 2 * 4 * 1.2 / MB:.1f}MB · ID {n * 52 / MB:.1f}MB")


if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=VectorParams(size=dim, distance=Distance.COSINE))
client.upload_collection(N, vectors=vecs, ids=range(n), batch_size=500, wait=True)
while (info := client.get_collection(N)).status != CollectionStatus.GREEN or info.indexed_vectors_count < 0.9 * n:
    time.sleep(1)
time.sleep(10)


mem = requests.get(f"http://localhost:6333/collections/{N}/memory").json()["result"]
show = lambda name, part: print(f"{name:7} · 디스크 {part['disk_bytes'] / MB:6.1f}MB · RAM {part['ram_bytes'] / MB:4.1f}MB · 있어야 할 캐시 {part['expected_cache_bytes'] / MB:6.1f}MB")
show("벡터", mem["vectors"][0]["storage"])
show("HNSW", mem["vectors"][0]["index"])
show("ID", mem["other"]["id_tracker"])
show("payload", mem["payload"])
show("합계", mem["total"])
print(subprocess.run(["docker", "exec", "qdrant-course", "du", "-sh", f"/qdrant/storage/collections/{N}"], capture_output=True, text=True).stdout)
