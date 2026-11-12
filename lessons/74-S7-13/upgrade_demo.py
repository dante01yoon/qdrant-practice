import subprocess
import time

import numpy as np
import requests
from qdrant_client import QdrantClient, models

U = "http://localhost:6410"
vecs = np.load("product_vecs.npy", mmap_mode="r")[:2000]


def start(image):
    subprocess.run(["docker", "rm", "-f", "qd-upg"], capture_output=True)
    subprocess.run(["docker", "run", "-d", "--name", "qd-upg", "-p", "6410:6333", "-v", "qd_upg:/qdrant/storage", image], capture_output=True)
    for _ in range(60):
        try:
            if requests.get(f"{U}/readyz", timeout=1).status_code == 200:
                break
        except requests.RequestException:
            pass
        time.sleep(1)
    print("버전", requests.get(U).json()["version"])


subprocess.run(["docker", "volume", "rm", "-f", "qd_upg"], capture_output=True)
start("qdrant/qdrant:v1.19.0")
client = QdrantClient(url=U, check_compatibility=False)
client.create_collection("up", vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE))
client.upload_collection("up", vectors=vecs, ids=range(len(vecs)), batch_size=256, wait=True)
before = {p.id for p in client.query_points("up", query=vecs[0].tolist(), limit=10).points}


start("qdrant/qdrant:v1.20.0")
print("점", client.count("up", exact=True).count)
print("결과 같음", before == {p.id for p in client.query_points("up", query=vecs[0].tolist(), limit=10).points})

subprocess.run(["docker", "rm", "-f", "qd-upg"], capture_output=True)
subprocess.run(["docker", "volume", "rm", "-f", "qd_upg"], capture_output=True)
