import uuid
import numpy as np, pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
p = pd.read_parquet("products.parquet"); v = np.load("product_vecs.npy", mmap_mode="r")
c = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
if c.collection_exists("products_uuid"): c.delete_collection("products_uuid")
c.create_collection("products_uuid", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))
for s in range(0, len(p), 500):
    c.upsert("products_uuid", points=[PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{r.product_id}")), vector=v[i].tolist(), payload={"product_id": r.product_id, "title": r.product_title}) for i, r in enumerate(p.iloc[s:s + 500].itertuples(), start=s)])
