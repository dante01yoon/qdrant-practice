import time

import numpy as np
from qdrant_client.models import Prefetch

from fusion_eval import client, ndcg10, queries, query_vecs

N = "products_colbert"
q_tokens = np.load("colbert_q_tokens.npy")
q_starts = np.concatenate([[0], np.cumsum(np.load("colbert_q_lens.npy"))])

WAYS = {
    "dense만": lambda i: dict(query=query_vecs[i].tolist(), using="dense"),
    "dense 50개 → colbert": lambda i: dict(prefetch=[Prefetch(query=query_vecs[i].tolist(), using="dense", limit=50)],
                                          query=q_tokens[q_starts[i]:q_starts[i + 1]].tolist(), using="colbert"),
}
for name, make in WAYS.items():
    scores, times = [], []
    for i, q in enumerate(queries.itertuples()):
        t0 = time.perf_counter()
        hits = client.query_points(N, limit=10, with_payload=["product_id"], **make(i)).points
        times.append(time.perf_counter() - t0)
        scores.append(ndcg10(q.query_id, [h.payload["product_id"] for h in hits]))
    print(f"{name:20} nDCG@10 {np.mean(scores):.3f} · 가운데 {np.median(times) * 1000:.1f}ms")
