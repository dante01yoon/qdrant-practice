import subprocess
import time

import numpy as np
import requests
from qdrant_client import QdrantClient, models

U = "http://localhost:6401"
client = QdrantClient(url=U, timeout=30)
N = "products_cluster"
vecs = np.load("product_vecs.npy", mmap_mode="r")
queries = np.load("query_vecs.npy")[:100]


def states():
    info = requests.get(f"{U}/collections/{N}/cluster").json()["result"]
    return sorted({s["state"] for s in info["local_shards"] + info["remote_shards"]})


def try_search():
    ok = 0
    for q in queries:
        try:
            client.query_points(N, query=q.tolist(), limit=10)
            ok += 1
        except Exception:
            pass
    return f"검색 {ok}/100 성공"


print("처음", states(), try_search())

subprocess.run(["docker", "stop", "qd-node3"], capture_output=True)
print("노드 하나 내림", try_search())
client.upsert(N, points=[models.PointStruct(id=99999, vector=vecs[0].tolist())], wait=True)
time.sleep(3)
print("쓰기 성공 · 상태", states())

subprocess.run(["docker", "start", "qd-node3"], capture_output=True)
t0 = time.time()
while states() != ["Active"]:
    time.sleep(1)
print(f"복귀 {time.time() - t0:.0f}초 · 상태", states())
