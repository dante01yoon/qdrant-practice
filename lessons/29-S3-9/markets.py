import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, FieldCondition, Filter, MatchValue, PayloadSchemaType, PointStruct, VectorParams

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_markets"

if not client.collection_exists(N):
    client.create_collection(N, vectors_config=VectorParams(size=1024, distance=Distance.COSINE))
    client.create_payload_index(N, "market", PayloadSchemaType.KEYWORD)
    us, us_vecs = pd.read_parquet("products.parquet"), np.load("product_vecs.npy")
    other, other_vecs = pd.read_parquet("market_products.parquet"), np.load("market_vecs.npy")
    rows = [("us", r.product_id, r.product_title, us_vecs[i]) for i, r in enumerate(us.itertuples())]
    rows += [(r.product_locale, r.product_id, r.product_title, other_vecs[i]) for i, r in enumerate(other.itertuples())]
    points = [PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{mk}/{pid}")), vector=v.tolist(), payload={"market": mk, "title": t})
              for mk, pid, t, v in rows]
    client.upload_points(N, points=points, batch_size=256, wait=True)

for market in ["us", "es", "jp"]:
    print(market, client.count(N, count_filter=Filter(must=[FieldCondition(key="market", match=MatchValue(value=market))])).count)
