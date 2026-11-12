import numpy as np
from qdrant_client.models import Rrf, RrfQuery

from fusion_eval import N, both, client, ndcg10, queries, query_vecs


def score(weights):
    found = []
    for i, q in enumerate(queries.itertuples()):
        hits = client.query_points(N, prefetch=both(query_vecs[i].tolist(), q.query), query=RrfQuery(rrf=Rrf(k=60, weights=weights)),
                                   limit=10, with_payload=["product_id"]).points
        found.append(ndcg10(q.query_id, [h.payload["product_id"] for h in hits]))
    return np.mean(found)


for w in [[1, 1], [1, 2], [1, 3], [1, 4], [1, 8]]:
    print(f"dense {w[0]} : sparse {w[1]} → {score(w):.3f}")
