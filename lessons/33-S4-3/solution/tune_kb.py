import uuid

import numpy as np
import pandas as pd
from qdrant_client.models import Modifier, PointStruct, SparseVectorParams

from bm25 import bm25_doc, bm25_query, client, docs, products

queries = pd.read_csv("queries.csv")
qrels = pd.read_csv("qrels.csv")
GAIN = {"E": 1.0, "S": 0.1, "C": 0.01, "I": 0.0}
TRY = "products_bm25_try"


def ndcg10(query_id, found):
    rel = {r.product_id: GAIN[r.esci_label] for r in qrels[qrels["query_id"] == query_id].itertuples()}
    dcg = sum(rel.get(p, 0) / np.log2(k + 2) for k, p in enumerate(found))
    ideal = sorted(rel.values(), reverse=True)[:10]
    return dcg / sum(g / np.log2(k + 2) for k, g in enumerate(ideal))


def score(k1, b):
    if client.collection_exists(TRY):
        client.delete_collection(TRY)
    client.create_collection(TRY, vectors_config={}, sparse_vectors_config={"bm25": SparseVectorParams(modifier=Modifier.IDF)})
    client.upload_points(TRY, points=[PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{r.product_id}")),
                                                  vector={"bm25": bm25_doc(d, k1, b)}, payload={"product_id": r.product_id})
                                      for r, d in zip(products.itertuples(), docs)], batch_size=256, wait=True)
    found = [[h.payload["product_id"] for h in client.query_points(TRY, query=bm25_query(q.query), using="bm25", limit=10).points]
             for q in queries.itertuples()]
    return np.mean([ndcg10(q.query_id, f) for q, f in zip(queries.itertuples(), found)])


if __name__ == "__main__":
    for k1, b in [(1.2, 0.75), (1.2, 0.0), (2.0, 0.75), (0.5, 0.75)]:
        print(f"k1={k1} b={b} → nDCG@10 {score(k1, b):.3f}")
