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
    return [{p.id for p in client.query_points(N, query=q.tolist(), limit=10, search_params=params).points} for q in queries]


truth = run(SearchParams(exact=True))
for ef in [16, 64, 256]:
    got = run(SearchParams(hnsw_ef=ef))
    per = np.array([len(g & t) / 10 for g, t in zip(got, truth)])
    print(f"hnsw_ef {ef:3} · 평균 {per.mean():.3f} · 가장 나쁜 질문 {per.min():.1f} · 0.7 이하인 질문 {(per <= 0.7).sum()}개 / {len(per)}개")
client.delete_collection(N)
