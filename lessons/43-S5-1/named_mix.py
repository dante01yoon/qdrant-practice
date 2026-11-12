import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Fusion, FusionQuery, Prefetch

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


def mix(names, fusion):
    return lambda v: dict(prefetch=[Prefetch(query=v, using=n, limit=50) for n in names], query=FusionQuery(fusion=fusion))


WAYS = {
    "all 한 덩어리": lambda v: dict(query=v, using="all"),
    "title만": lambda v: dict(query=v, using="title"),
    "title + detail · RRF": mix(["title", "detail"], Fusion.RRF),
    "title + detail · DBSF": mix(["title", "detail"], Fusion.DBSF),
    "셋 다 · DBSF": mix(["all", "title", "detail"], Fusion.DBSF),
}
for name, make in WAYS.items():
    scores = [ndcg10(q.query_id, [h.payload["product_id"] for h in client.query_points(N, limit=10, with_payload=["product_id"], **make(query_vecs[i].tolist())).points])
              for i, q in enumerate(queries.itertuples())]
    print(f"{name:22} nDCG@10 = {np.mean(scores):.3f}")
