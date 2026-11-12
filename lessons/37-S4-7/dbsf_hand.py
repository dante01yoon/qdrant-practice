import numpy as np
import pandas as pd
from qdrant_client.models import Fusion, FusionQuery, Prefetch

from bm25 import bm25_query, client

N = "products_hybrid"
text = "non metal cooking utensils"
queries = pd.read_csv("queries.csv")
vec = np.load("query_vecs.npy")[queries.index[queries["query"] == text][0]].tolist()
dense = client.query_points(N, query=vec, using="dense", limit=10).points
sparse = client.query_points(N, query=bm25_query(text), using="bm25", limit=10).points


def normalize(hits):
    scores = np.array([h.score for h in hits])
    low = scores.mean() - 3 * scores.std(ddof=1)
    high = scores.mean() + 3 * scores.std(ddof=1)
    return {h.id: (h.score - low) / (high - low) for h in hits}


a, b = normalize(dense), normalize(sparse)
mine = sorted(((pid, a.get(pid, 0) + b.get(pid, 0)) for pid in set(a) | set(b)), key=lambda x: -x[1])[:3]
theirs = client.query_points(N, prefetch=[Prefetch(query=vec, using="dense", limit=10), Prefetch(query=bm25_query(text), using="bm25", limit=10)],
                             query=FusionQuery(fusion=Fusion.DBSF), limit=3).points
print("벡터 점수 범위:", round(dense[-1].score, 3), "~", round(dense[0].score, 3), "/ BM25 점수 범위:", round(sparse[-1].score, 2), "~", round(sparse[0].score, 2))
for (pid, s), h in zip(mine, theirs):
    print(f"내 계산 {s:.4f} · Qdrant {h.score:.4f} · 같은 상품 {pid == h.id}")
