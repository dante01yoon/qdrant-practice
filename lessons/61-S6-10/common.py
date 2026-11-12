import numpy as np
import pandas as pd

queries = pd.read_csv("queries.csv")
query_vecs = np.load("query_vecs.npy")
qrels = pd.read_csv("qrels.csv")
GAIN = {"E": 1.0, "S": 0.1, "C": 0.01, "I": 0.0}


def ndcg10(query_id, found):
    rel = {r.product_id: GAIN[r.esci_label] for r in qrels[qrels["query_id"] == query_id].itertuples()}
    dcg = sum(rel.get(p, 0) / np.log2(k + 2) for k, p in enumerate(found))
    ideal = sorted(rel.values(), reverse=True)[:10]
    return dcg / sum(g / np.log2(k + 2) for k, g in enumerate(ideal))


def rrf(lists, k=60):
    score = {}
    for found in lists:
        for rank, p in enumerate(found):
            score[p] = score.get(p, 0) + 1 / (k + rank + 1)
    return [p for p, _ in sorted(score.items(), key=lambda x: -x[1])][:10]
