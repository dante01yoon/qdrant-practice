import time

import numpy as np
from qdrant_client.models import Prefetch

from fusion_eval import client, ndcg10, queries, query_vecs

N = "products_colbert"
q_tokens = np.load("colbert_q_tokens.npy")
q_starts = np.concatenate([[0], np.cumsum(np.load("colbert_q_lens.npy"))])


def colbert(i, candidates):
    return dict(prefetch=[Prefetch(query=query_vecs[i].tolist(), using="dense", limit=candidates)],
                query=q_tokens[q_starts[i]:q_starts[i + 1]].tolist(), using="colbert")


for candidates in [20, 50, 100, 300]:
    scores, times = [], []
    for i, q in enumerate(queries.itertuples()):
        t0 = time.perf_counter()
        hits = client.query_points(N, limit=10, with_payload=["product_id"], **colbert(i, candidates)).points
        times.append(time.perf_counter() - t0)
        scores.append(ndcg10(q.query_id, [h.payload["product_id"] for h in hits]))
    print(f"dense 후보 {candidates:3}개 → colbert · nDCG@10 {np.mean(scores):.3f} · 가운데 {np.median(times) * 1000:.1f}ms")
