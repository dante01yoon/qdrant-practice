import numpy as np
import pandas as pd
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_named"
products = pd.read_parquet("products.parquet")
queries = pd.read_csv("queries.csv")
query_vecs = np.load("query_vecs.npy")
qrels = pd.read_csv("qrels.csv")
GAIN = {"E": 1.0, "S": 0.1, "C": 0.01, "I": 0.0}


def ndcg10(query_id, found):
    rel = {r.product_id: GAIN[r.esci_label] for r in qrels[qrels["query_id"] == query_id].itertuples()}
    dcg = sum(rel.get(p, 0) / np.log2(k + 2) for k, p in enumerate(found))
    ideal = sorted(rel.values(), reverse=True)[:10]
    return dcg / sum(g / np.log2(k + 2) for k, g in enumerate(ideal))


has_detail = set(products.product_id[products.product_bullet_point.notna()])
exact = qrels[qrels.esci_label == "E"]
fair = [q for q in queries.itertuples() if set(exact.product_id[exact.query_id == q.query_id]) <= has_detail]
print("검색어", len(queries), "개 중 정답 상품이 모두 특징을 가진 검색어:", len(fair))

for name in ["title", "detail"]:
    scores = []
    for q in fair:
        hits = client.query_points(N, query=query_vecs[q.Index].tolist(), using=name, limit=10, with_payload=["product_id"]).points
        scores.append(ndcg10(q.query_id, [h.payload["product_id"] for h in hits]))
    print(f"{name:6} nDCG@10 = {np.mean(scores):.3f}")
