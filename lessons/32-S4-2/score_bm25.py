import numpy as np
import pandas as pd

from bm25 import N, bm25_query, client

queries = pd.read_csv("queries.csv")
qrels = pd.read_csv("qrels.csv")
GAIN = {"E": 1.0, "S": 0.1, "C": 0.01, "I": 0.0}


def ndcg10(query_id, found):
    rel = {r.product_id: GAIN[r.esci_label] for r in qrels[qrels["query_id"] == query_id].itertuples()}
    dcg = sum(rel.get(p, 0) / np.log2(k + 2) for k, p in enumerate(found))
    ideal = sorted(rel.values(), reverse=True)[:10]
    return dcg / sum(g / np.log2(k + 2) for k, g in enumerate(ideal))


scores = []
for q in queries.itertuples():
    hits = client.query_points(N, query=bm25_query(q.query), using="bm25", limit=10).points
    scores.append(ndcg10(q.query_id, [h.payload["product_id"] for h in hits]))
print(f"BM25 sparse nDCG@10 = {np.mean(scores):.3f}")
