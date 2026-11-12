import json
import os
import re
import uuid
from collections import Counter

import numpy as np
import pandas as pd
import requests
from qdrant_client import QdrantClient, models

URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
GRPC = int(os.environ.get("QDRANT_GRPC", "6334"))
client = QdrantClient(url=URL, grpc_port=GRPC, prefer_grpc=True, timeout=120)


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


products = pd.read_parquet("products.parquet").fillna("")
vecs = np.load("product_vecs.npy")
docs = [tokens(" ".join([r.product_title, r.product_brand, r.product_color, r.product_bullet_point[:600]])) for r in products.itertuples()]
vocab = {}
for doc in docs:
    for t in doc:
        vocab.setdefault(t, len(vocab))
json.dump(vocab, open("shop_vocab.json", "w"))
avg_len = sum(map(len, docs)) / len(docs)
print("상품", len(docs), "· 사전 단어", len(vocab))


def bm25(doc, k1=1.2, b=0.75):
    tf = Counter(doc)
    norm = k1 * (1 - b + b * len(doc) / avg_len)
    return models.SparseVector(indices=[vocab[t] for t in tf], values=[f * (k1 + 1) / (f + norm) for f in tf.values()])


SHOP = "shop_v1"
if client.collection_exists(SHOP):
    client.delete_collection(SHOP)
client.create_collection(SHOP, vectors_config={"dense": models.VectorParams(size=1024, distance=models.Distance.COSINE)},
                         sparse_vectors_config={"bm25": models.SparseVectorParams(modifier=models.Modifier.IDF)})
client.create_payload_index(SHOP, "product_brand", models.PayloadSchemaType.KEYWORD)
client.create_payload_index(SHOP, "product_color", models.PayloadSchemaType.KEYWORD)
points = [models.PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{r.product_id}")), vector={"dense": v.tolist(), "bm25": bm25(d)},
                             payload={"product_id": r.product_id, "title": r.product_title, "product_brand": r.product_brand, "product_color": r.product_color})
          for r, v, d in zip(products.itertuples(), vecs, docs)]
client.upload_points(SHOP, points=points, batch_size=256, wait=True)
print("shop_v1", client.count(SHOP, exact=True).count)

HELP = "help_v1"
if client.collection_exists(HELP):
    client.delete_collection(HELP)
with open("wix_hybrid.snapshot", "rb") as f:
    requests.post(f"{URL}/collections/{HELP}/snapshots/upload?priority=snapshot", files={"snapshot": f}, timeout=600).raise_for_status()
print("help_v1", client.count(HELP, exact=True).count)

client.update_collection_aliases([
    models.CreateAliasOperation(create_alias=models.CreateAlias(collection_name=SHOP, alias_name="shop")),
    models.CreateAliasOperation(create_alias=models.CreateAlias(collection_name=HELP, alias_name="help")),
])
print("별칭", sorted(a.alias_name for a in client.get_aliases().aliases))
