import sys

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Fusion, FusionQuery, Prefetch, Rrf, RrfQuery

from bm25 import bm25_query

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_hybrid"
queries = pd.read_csv("queries.csv")
query_vecs = np.load("query_vecs.npy")
qrels = pd.read_csv("qrels.csv")
GAIN = {"E": 1.0, "S": 0.1, "C": 0.01, "I": 0.0}


def ndcg10(query_id, found):
    rel = {r.product_id: GAIN[r.esci_label] for r in qrels[qrels["query_id"] == query_id].itertuples()}
    dcg = sum(rel.get(p, 0) / np.log2(k + 2) for k, p in enumerate(found))
    ideal = sorted(rel.values(), reverse=True)[:10]
    return dcg / sum(g / np.log2(k + 2) for k, g in enumerate(ideal))


METHODS = {
    "dense": lambda v, t: dict(query=v, using="dense"),
    "sparse": lambda v, t: dict(query=bm25_query(t), using="bm25"),
    "rrf k=2": lambda v, t: dict(prefetch=both(v, t), query=FusionQuery(fusion=Fusion.RRF)),
    "rrf k=60": lambda v, t: dict(prefetch=both(v, t), query=RrfQuery(rrf=Rrf(k=60))),
    "dbsf": lambda v, t: dict(prefetch=both(v, t), query=FusionQuery(fusion=Fusion.DBSF)),
}


def both(v, t):
    return [Prefetch(query=v, using="dense", limit=50), Prefetch(query=bm25_query(t), using="bm25", limit=50)]


for name in sys.argv[1:]:
    scores = []
    for i, q in enumerate(queries.itertuples()):
        hits = client.query_points(N, limit=10, with_payload=["product_id"], **METHODS[name](query_vecs[i].tolist(), q.query)).points
        scores.append(ndcg10(q.query_id, [h.payload["product_id"] for h in hits]))
    print(f"{name:9} nDCG@10 = {np.mean(scores):.3f}")
