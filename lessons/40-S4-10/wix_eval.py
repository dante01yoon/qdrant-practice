import json
import re

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Fusion, FusionQuery, Prefetch, Rrf, RrfQuery, SparseVector

from embed import embed

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "wix_hybrid"
questions = [json.loads(line) for line in open("wixqa_expertwritten_test.jsonl")]


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


vocab = json.load(open("wix_vocab.json"))


def sparse(text):
    ids = sorted({vocab[t] for t in tokens(text) if t in vocab})
    return SparseVector(indices=ids, values=[1.0] * len(ids))


def both(v, s):
    return [Prefetch(query=v, using="dense", limit=50), Prefetch(query=s, using="bm25", limit=50)]


WAYS = {
    "dense": lambda v, s: dict(query=v, using="dense"),
    "sparse": lambda v, s: dict(query=s, using="bm25"),
    "RRF 1:1": lambda v, s: dict(prefetch=both(v, s), query=RrfQuery(rrf=Rrf(k=60, weights=[1, 1]))),
    "RRF 1:2": lambda v, s: dict(prefetch=both(v, s), query=RrfQuery(rrf=Rrf(k=60, weights=[1, 2]))),
    "DBSF": lambda v, s: dict(prefetch=both(v, s), query=FusionQuery(fusion=Fusion.DBSF)),
}
asked = [(embed(q["question"]), sparse(q["question"]), set(q["article_ids"])) for q in questions]
for name, make in WAYS.items():
    hit = [bool(gold & {h.payload["article_id"] for h in client.query_points(N, limit=5, with_payload=["article_id"], **make(v, s)).points})
           for v, s, gold in asked]
    print(f"{name:8} recall@5 = {np.mean(hit):.3f}")
