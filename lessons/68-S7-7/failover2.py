import subprocess
import time

import numpy as np
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6401", timeout=10)
N = "products_cluster"
vec = np.load("query_vecs.npy")[0].tolist()


def attempt(title, fn):
    try:
        fn()
        print(title, "성공")
    except Exception as e:
        print(title, "실패:", str(e).split("\n")[0][:60])


subprocess.run(["docker", "stop", "qd-node2", "qd-node3"], capture_output=True)
time.sleep(5)
attempt("검색", lambda: client.query_points(N, query=vec, limit=10))
attempt("컬렉션 만들기", lambda: client.create_collection("x_try", vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE), timeout=5))

subprocess.run(["docker", "start", "qd-node2", "qd-node3"], capture_output=True)
time.sleep(20)
attempt("다시 검색", lambda: client.query_points(N, query=vec, limit=10))
