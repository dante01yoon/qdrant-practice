import json
import re
import time

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Fusion, FusionQuery, Prefetch, SparseVector
from sentence_transformers import CrossEncoder

from embed import embed

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "wix_hybrid"
questions = [json.loads(line) for line in open("wixqa_expertwritten_test.jsonl")]
vocab = json.load(open("wix_vocab.json"))
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=512)


def sparse(text):
    ids = sorted({vocab[t] for t in re.findall(r"[a-z0-9]+", text.lower()) if t in vocab})
    return SparseVector(indices=ids, values=[1.0] * len(ids))


before, after, t_total = [], [], 0.0
for q in questions:
    hits = client.query_points(N, prefetch=[Prefetch(query=embed(q["question"]), using="dense", limit=50), Prefetch(query=sparse(q["question"]), using="bm25", limit=50)],
                               query=FusionQuery(fusion=Fusion.DBSF), limit=20, with_payload=["article_id", "text"]).points
    gold = set(q["article_ids"])
    before.append(bool(gold & {h.payload["article_id"] for h in hits[:5]}))
    t0 = time.perf_counter()
    scores = reranker.predict([(q["question"], h.payload["text"]) for h in hits], batch_size=20)
    t_total += time.perf_counter() - t0
    after.append(bool(gold & {hits[j].payload["article_id"] for j in np.argsort(-scores)[:5]}))
print(f"DBSF recall@5 {np.mean(before):.3f} → 리랭커 {np.mean(after):.3f} · 리랭커 질문당 {t_total / len(questions) * 1000:.0f}ms")
