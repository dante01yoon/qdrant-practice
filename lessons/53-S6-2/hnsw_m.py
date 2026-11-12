import time

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import CollectionStatus, Distance, HnswConfigDiff, SearchParams, VectorParams

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, timeout=600)
vecs = np.load("vecs_100k.npy", mmap_mode="r")
queries = np.load("query_vecs.npy")[:200]
N = "hnsw_test"


def build(m, ef_construct):
    if client.collection_exists(N):
        client.delete_collection(N)
    client.create_collection(N, vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
                             hnsw_config=HnswConfigDiff(m=m, ef_construct=ef_construct))
    client.upload_collection(N, vectors=vecs, ids=range(len(vecs)), batch_size=500, wait=True)
    while (info := client.get_collection(N)).status != CollectionStatus.GREEN or info.indexed_vectors_count < 0.9 * len(vecs):
        time.sleep(0.5)


def run(params):
    return [{p.id for p in client.query_points(N, query=q.tolist(), limit=10, search_params=params).points} for q in queries]


def recall(got, truth):
    return np.mean([len(g & t) / 10 for g, t in zip(got, truth)])


truth = None
for m in [4, 16, 32]:
    build(m, 100)
    truth = truth or run(SearchParams(exact=True))
    print(f"m={m:2} · ef_construct=100 · recall@10 {recall(run(SearchParams(hnsw_ef=64)), truth):.3f}")
