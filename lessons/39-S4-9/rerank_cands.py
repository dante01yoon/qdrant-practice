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


def search(i, q, candidates):
    hits = client.query_points(N, prefetch=both(query_vecs[i].tolist(), q.query), query=FusionQuery(fusion=Fusion.DBSF),
                               limit=candidates, with_payload=["product_id"]).points
    ids = [h.payload["product_id"] for h in hits]
    scores = reranker.predict([(q.query, text(pid)) for pid in ids], batch_size=50)
    return [ids[j] for j in np.argsort(-scores)][:10]


for candidates in [10, 20, 50]:
    t0 = time.perf_counter()
    scores = [ndcg10(q.query_id, search(i, q, candidates)) for i, q in enumerate(queries.head(100).itertuples())]
    print(f"후보 {candidates:2}개 · nDCG@10 {np.mean(scores):.3f} · 질문당 {(time.perf_counter() - t0) / 100 * 1000:.0f}ms")
