import numpy as np

from bm25 import tokens, vocab
from fusion_eval import METHODS, N, client, ndcg10, queries, query_vecs


def run(name, i, q):
    hits = client.query_points(N, limit=10, with_payload=["product_id"], **METHODS[name](query_vecs[i].tolist(), q.query)).points
    return ndcg10(q.query_id, [h.payload["product_id"] for h in hits])


def known_words(text):
    return sum(t in vocab for t in tokens(text))


rows = [(run("dense", i, q), run("dbsf", i, q), known_words(q.query), len(tokens(q.query))) for i, q in enumerate(queries.itertuples())]
dense, dbsf, known, total = map(np.array, zip(*rows))
print(f"늘 dense {dense.mean():.3f} · 늘 DBSF {dbsf.mean():.3f} · 질문마다 더 나은 쪽 {np.maximum(dense, dbsf).mean():.3f}")
for need in [1, 2, 3]:
    routed = np.where(known >= need, dbsf, dense)
    print(f"사전 단어 {need}개 이상일 때만 섞기 → {routed.mean():.3f} (섞은 검색어 {(known >= need).sum()}개)")
missing = total - known
routed = np.where(missing == 0, dbsf, dense)
print(f"모든 단어가 사전에 있을 때만 섞기 → {routed.mean():.3f} (섞은 검색어 {(missing == 0).sum()}개)")
