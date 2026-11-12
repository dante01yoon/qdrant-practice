import json
import re
import time

import numpy as np
from qdrant_client import QdrantClient, models
from sentence_transformers import CrossEncoder, SentenceTransformer

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
t = time.perf_counter()
model = SentenceTransformer("BAAI/bge-m3")
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=512)
print(f"모델 불러오기 {time.perf_counter() - t:.0f}초")
questions = [json.loads(line)["question"] for line in open("wixqa_expertwritten_test.jsonl")][:30]
vocab = json.load(open("wix_vocab.json"))

spent = {"벡터 만들기": [], "Qdrant 찾기": [], "리랭커": []}
for q in questions:
    t = time.perf_counter()
    v = model.encode(q, normalize_embeddings=True).tolist()
    spent["벡터 만들기"].append(time.perf_counter() - t)
    ids = sorted({vocab[w] for w in re.findall(r"[a-z0-9]+", q.lower()) if w in vocab})
    s = models.SparseVector(indices=ids, values=[1.0] * len(ids))
    t = time.perf_counter()
    hits = client.query_points("wix_hybrid", limit=20, prefetch=[models.Prefetch(query=v, using="dense", limit=50), models.Prefetch(query=s, using="bm25", limit=50)],
                               query=models.FusionQuery(fusion=models.Fusion.DBSF)).points
    spent["Qdrant 찾기"].append(time.perf_counter() - t)
    t = time.perf_counter()
    reranker.predict([(q, h.payload["text"]) for h in hits])
    spent["리랭커"].append(time.perf_counter() - t)

for name, times in spent.items():
    print(f"{name} · 가운데 {np.median(times) * 1000:.0f}ms · 느린 쪽 {np.percentile(times, 95) * 1000:.0f}ms")
