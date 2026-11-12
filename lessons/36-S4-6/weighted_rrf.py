import numpy as np
import pandas as pd
from qdrant_client.models import Prefetch, Rrf, RrfQuery

from bm25 import bm25_query, client

N = "products_hybrid"
text = "non metal cooking utensils"
queries = pd.read_csv("queries.csv")
vec = np.load("query_vecs.npy")[queries.index[queries["query"] == text][0]].tolist()

dense = [h.id for h in client.query_points(N, query=vec, using="dense", limit=10).points]
sparse = [h.id for h in client.query_points(N, query=bm25_query(text), using="bm25", limit=10).points]


def rrf(lists, weights, k=2):
    scores = {}
    for ranking, w in zip(lists, weights):
        for r, pid in enumerate(ranking):
            scores[pid] = scores.get(pid, 0) + 1 / (k + (r + 1) / w - 1)
    return sorted(scores.items(), key=lambda x: -x[1])


mine = rrf([dense, sparse], [2, 1])[:3]
theirs = client.query_points(N, prefetch=[Prefetch(query=vec, using="dense", limit=10), Prefetch(query=bm25_query(text), using="bm25", limit=10)],
                             query=RrfQuery(rrf=Rrf(k=2, weights=[2, 1])), limit=3).points
for (pid, s), h in zip(mine, theirs):
    print(f"내 계산 {s:.4f} · Qdrant {h.score:.4f} · 같은 상품 {pid == h.id}")
