import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Prefetch, Rrf, RrfQuery

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_final"
queries = pd.read_csv("queries.csv")
query_vecs = np.load("query_vecs.npy")
qrels = pd.read_csv("qrels.csv")
GAIN = {"E": 1.0, "S": 0.1, "C": 0.01, "I": 0.0}


def ndcg10(query_id, found):
    rel = {r.product_id: GAIN[r.esci_label] for r in qrels[qrels["query_id"] == query_id].itertuples()}
    dcg = sum(rel.get(p, 0) / np.log2(k + 2) for k, p in enumerate(found))
    ideal = sorted(rel.values(), reverse=True)[:10]
    return dcg / sum(g / np.log2(k + 2) for k, g in enumerate(ideal))


def score(weights):
    found = []
    for i, q in enumerate(queries.itertuples()):
        v = query_vecs[i].tolist()
        hits = client.query_points(N, prefetch=[Prefetch(query=v, using="all", limit=50), Prefetch(query=v, using="title", limit=50)],
                                   query=RrfQuery(rrf=Rrf(k=60, weights=weights)), limit=10, with_payload=["product_id"]).points
        found.append(ndcg10(q.query_id, [h.payload["product_id"] for h in hits]))
    return np.mean(found)


for w in [[1, 1], [2, 1], [3, 1], [1, 2]]:
    print(f"all {w[0]} : title {w[1]} → nDCG@10 {score(w):.3f}")
