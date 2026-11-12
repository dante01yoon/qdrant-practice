import subprocess
import time

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6401", timeout=60)
N = "market_products"

us, us_vecs = pd.read_parquet("products.parquet"), np.load("product_vecs.npy")
other, other_vecs = pd.read_parquet("market_products.parquet"), np.load("market_vecs.npy")
vecs = np.concatenate([us_vecs, other_vecs])
markets = ["us"] * len(us) + other.product_locale.tolist()

if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
                         shard_number=6, replication_factor=2)
client.create_payload_index(N, "market", field_schema=models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD, is_tenant=True))
client.upload_collection(N, vectors=vecs, payload=[{"market": m} for m in markets], ids=range(len(vecs)), batch_size=256, wait=True)
print("점", client.count(N, exact=True).count)


def search(market):
    only = models.Filter(must=[models.FieldCondition(key="market", match=models.MatchValue(value=market))])
    return [p.payload["market"] for p in client.query_points(N, query=vecs[0].tolist(), query_filter=only, limit=5, with_payload=True).points]


print("평소 jp", search("jp"))
subprocess.run(["docker", "stop", "qd-node2"], capture_output=True)
print("한 대 끔 jp", search("jp"))
print("한 대 끔 es", search("es"))
subprocess.run(["docker", "start", "qd-node2"], capture_output=True)
time.sleep(10)
print("복귀 us", search("us"))
