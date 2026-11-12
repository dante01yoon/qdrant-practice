import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Fusion, FusionQuery, Prefetch

from bm25 import bm25_query

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_hybrid"
text = "non metal cooking utensils"
queries = pd.read_csv("queries.csv")
dense = np.load("query_vecs.npy")[queries.index[queries["query"] == text][0]].tolist()

d_ids = [h.id for h in client.query_points(N, query=dense, using="dense", limit=10).points]
s_ids = [h.id for h in client.query_points(N, query=bm25_query(text), using="bm25", limit=10).points]


def rrf(rankings, k=2):
    score = {}
    for ranking in rankings:
        for rank, pid in enumerate(ranking):
            score[pid] = score.get(pid, 0) + 1 / (k + rank)
    return sorted(score.items(), key=lambda x: -x[1])


mine = rrf([d_ids, s_ids])[:3]
fused = client.query_points(N, prefetch=[Prefetch(query=dense, using="dense", limit=10), Prefetch(query=bm25_query(text), using="bm25", limit=10)],
                            query=FusionQuery(fusion=Fusion.RRF), limit=3, with_payload=["title"]).points
for (pid, s), h in zip(mine, fused):
    print(f"손계산 {s:.4f} | Qdrant {h.score:.4f} | 벡터 {d_ids.index(pid) + 1 if pid in d_ids else '-'}위 · 단어 {s_ids.index(pid) + 1 if pid in s_ids else '-'}위 | {h.payload['title'][:30]}")
