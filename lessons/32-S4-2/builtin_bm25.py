import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, TextIndexParams, TextIndexType, TextQuery, TokenizerType

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_text"
products = pd.read_parquet("products.parquet").fillna("")
queries = pd.read_csv("queries.csv")
qrels = pd.read_csv("qrels.csv")
GAIN = {"E": 1.0, "S": 0.1, "C": 0.01, "I": 0.0}


def ndcg10(query_id, found):
    rel = {r.product_id: GAIN[r.esci_label] for r in qrels[qrels["query_id"] == query_id].itertuples()}
    dcg = sum(rel.get(p, 0) / np.log2(k + 2) for k, p in enumerate(found))
    ideal = sorted(rel.values(), reverse=True)[:10]
    return dcg / sum(g / np.log2(k + 2) for k, g in enumerate(ideal))


if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config={})
client.create_payload_index(N, "text", TextIndexParams(type=TextIndexType.TEXT, tokenizer=TokenizerType.WORD, lowercase=True, scoring=True), wait=True)
client.upload_points(N, points=[
    PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{r.product_id}")), vector={},
                payload={"product_id": r.product_id, "text": " ".join([r.product_title, r.product_brand, r.product_color, r.product_bullet_point[:600]])})
    for r in products.itertuples()], batch_size=256, wait=True)

for h in client.query_points(N, query=TextQuery(text="eleven baby mask"), using="text", limit=3, with_payload=["text"]).points:
    print(f"  {h.score:.2f} {h.payload['text'][:50]}")
scores = [ndcg10(q.query_id, [h.payload["product_id"] for h in client.query_points(N, query=TextQuery(text=q.query), using="text", limit=10, with_payload=["product_id"]).points])
          for q in queries.itertuples()]
print("내장 BM25 nDCG@10:", round(np.mean(scores), 3))
