import time

import numpy as np
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333", timeout=300)
N = "snap_demo"
vecs = np.load("product_vecs.npy", mmap_mode="r")

if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE))
client.upload_collection(N, vectors=vecs, ids=range(len(vecs)), payload=[{"row": i} for i in range(len(vecs))], batch_size=500, wait=True)
print("점", client.count(N, exact=True).count)

t0 = time.perf_counter()
snap = client.create_snapshot(N)
print(f"스냅샷 {snap.size / 1024 / 1024:.0f}MB · {time.perf_counter() - t0:.1f}초")
print("이름", snap.name)
print("목록", [s.name[:30] for s in client.list_snapshots(N)])
