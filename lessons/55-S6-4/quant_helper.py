import time

import numpy as np
import requests
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, timeout=600)
vecs = np.load("vecs_100k.npy", mmap_mode="r")
queries = np.load("query_vecs.npy")[:200]
N = "quant_test"


def build(quant):
    if client.collection_exists(N):
        client.delete_collection(N)
    client.create_collection(N, vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE), quantization_config=quant)
    client.upload_collection(N, vectors=vecs, ids=range(len(vecs)), batch_size=500, wait=True)
    while (info := client.get_collection(N)).status != models.CollectionStatus.GREEN or info.indexed_vectors_count < 0.9 * len(vecs):
        time.sleep(0.5)
    time.sleep(5)


def run(params=None):
    got, ms = [], []
    for q in queries:
        t0 = time.perf_counter()
        got.append({p.id for p in client.query_points(N, query=q.tolist(), limit=10, search_params=params).points})
        ms.append((time.perf_counter() - t0) * 1000)
    return got, np.median(ms)


def recall(got, truth):
    return np.mean([len(g & t) / 10 for g, t in zip(got, truth)])


def size_mb():
    mem = requests.get(f"http://localhost:6333/collections/{N}/memory").json()["result"]["vectors"][0]
    return mem["quantized"]["disk_bytes"] / 1024 / 1024


def no_rescore():
    return models.SearchParams(quantization=models.QuantizationSearchParams(rescore=False))


def with_rescore(oversampling=2.0):
    return models.SearchParams(quantization=models.QuantizationSearchParams(rescore=True, oversampling=oversampling))
