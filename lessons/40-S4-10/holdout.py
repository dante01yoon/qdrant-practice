import json
import re

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Prefetch, Rrf, RrfQuery, SparseVector

from embed import embed

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "wix_hybrid"
questions = [json.loads(line) for line in open("wixqa_expertwritten_test.jsonl")]
vocab = json.load(open("wix_vocab.json"))


def sparse(text):
    ids = sorted({vocab[t] for t in re.findall(r"[a-z0-9]+", text.lower()) if t in vocab})
    return SparseVector(indices=ids, values=[1.0] * len(ids))


asked = [(embed(q["question"]), sparse(q["question"]), set(q["article_ids"])) for q in questions]
pick, check = asked[:100], asked[100:]


def recall5(group, weights):
    hit = []
    for v, s, gold in group:
        points = client.query_points(N, prefetch=[Prefetch(query=v, using="dense", limit=50), Prefetch(query=s, using="bm25", limit=50)],
                                     query=RrfQuery(rrf=Rrf(k=60, weights=weights)), limit=5, with_payload=["article_id"]).points
        hit.append(bool(gold & {p.payload["article_id"] for p in points}))
    return np.mean(hit)


WEIGHTS = [[1, 1], [1, 2], [2, 1], [3, 1]]
for w in WEIGHTS:
    print(f"무게 {w[0]}:{w[1]} · 고르는 100개 {recall5(pick, w):.2f} · 확인하는 100개 {recall5(check, w):.2f}")
