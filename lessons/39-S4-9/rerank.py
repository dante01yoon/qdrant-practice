import sys
import time

import numpy as np
import pandas as pd
from qdrant_client.models import Fusion, FusionQuery
from sentence_transformers import CrossEncoder

from fusion_eval import N, both, client, ndcg10, queries, query_vecs

products = pd.read_parquet("products.parquet").fillna("").set_index("product_id")
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=256)


def text(pid):
    p = products.loc[pid]
    return " ".join([p.product_title, p.product_brand, p.product_color, p.product_bullet_point[:600]])


def search(i, q, rerank):
    hits = client.query_points(N, prefetch=both(query_vecs[i].tolist(), q.query), query=FusionQuery(fusion=Fusion.DBSF),
                               limit=20, with_payload=["product_id"]).points
    ids = [h.payload["product_id"] for h in hits]
    if rerank:
        scores = reranker.predict([(q.query, text(pid)) for pid in ids], batch_size=20)
        ids = [ids[j] for j in np.argsort(-scores)]
    return ids[:10]


n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
for rerank in [False, True]:
    t0 = time.perf_counter()
    scores = [ndcg10(q.query_id, search(i, q, rerank)) for i, q in enumerate(queries.head(n).itertuples())]
    print(f"{'리랭커' if rerank else 'DBSF만':5} · 검색어 {n}개 · nDCG@10 {np.mean(scores):.3f} · 질문당 {(time.perf_counter() - t0) / n * 1000:.0f}ms")
