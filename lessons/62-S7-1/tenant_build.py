import numpy as np
import pandas as pd
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")
N = "market_products"

us, us_vecs = pd.read_parquet("products.parquet"), np.load("product_vecs.npy")
other, other_vecs = pd.read_parquet("market_products.parquet"), np.load("market_vecs.npy")
vecs = np.concatenate([us_vecs, other_vecs])
markets = ["us"] * len(us) + other.product_locale.tolist()
titles = us.product_title.tolist() + other.product_title.tolist()

if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
                         hnsw_config=models.HnswConfigDiff(payload_m=16, m=0))
client.create_payload_index(N, "market", field_schema=models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD, is_tenant=True))

payload = [{"market": m, "title": t} for m, t in zip(markets, titles)]
client.upload_collection(N, vectors=vecs, payload=payload, ids=range(len(vecs)), batch_size=256, wait=True)

for m in ["us", "es", "jp"]:
    only = models.Filter(must=[models.FieldCondition(key="market", match=models.MatchValue(value=m))])
    print(m, client.count(N, count_filter=only, exact=True).count)
print("전체", client.count(N, exact=True).count)
