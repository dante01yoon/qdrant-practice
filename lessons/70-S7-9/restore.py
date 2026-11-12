import time

import numpy as np
import requests
from qdrant_client import QdrantClient

U = "http://localhost:6333"
client = QdrantClient(url=U, timeout=300)
N = "snap_demo"
vec = np.load("product_vecs.npy", mmap_mode="r")[0].tolist()

before = {p.id for p in client.query_points(N, query=vec, limit=10).points}
name = client.list_snapshots(N)[-1].name

client.delete_collection(N)
print("지운 뒤 있나", client.collection_exists(N))

t0 = time.perf_counter()
r = requests.put(f"{U}/collections/{N}/snapshots/recover", json={"location": f"file:///qdrant/snapshots/{N}/{name}"}, timeout=300).json()
print(f"복구 {r['status']} · {time.perf_counter() - t0:.1f}초")

print("점", client.count(N, exact=True).count)
print("결과 같음", before == {p.id for p in client.query_points(N, query=vec, limit=10).points})
