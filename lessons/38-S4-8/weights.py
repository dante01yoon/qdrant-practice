import numpy as np
from qdrant_client.models import Fusion, FusionQuery, Prefetch, Rrf, RrfQuery

from bm25 import bm25_query
from fusion_eval import N, both, client, ndcg10, queries, query_vecs


def score(make):
    found = []
    for i, q in enumerate(queries.itertuples()):
        hits = client.query_points(N, limit=10, with_payload=["product_id"], **make(query_vecs[i].tolist(), q.query)).points
        found.append(ndcg10(q.query_id, [h.payload["product_id"] for h in hits]))
    return np.mean(found)


for w in [(1, 1), (2, 1), (1, 2), (3, 1)]:
    s = score(lambda v, t: dict(prefetch=both(v, t), query=RrfQuery(rrf=Rrf(k=60, weights=list(w)))))
    print(f"RRF 가중치 dense {w[0]} : sparse {w[1]} → {s:.3f}")


two_step = {
    "sparse 100개 → dense로 다시": lambda v, t: dict(prefetch=[Prefetch(query=bm25_query(t), using="bm25", limit=100)], query=v, using="dense"),
    "dense 100개 → sparse로 다시": lambda v, t: dict(prefetch=[Prefetch(query=v, using="dense", limit=100)], query=bm25_query(t), using="bm25"),
}
for name, make in two_step.items():
    print(f"{name} → {score(make):.3f}")
