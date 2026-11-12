import zlib

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PayloadSchemaType, PointStruct, VectorParams

ids = pd.read_parquet("us_product_ids.parquet", columns=["product_id"]).product_id[:100_000]
vectors = np.concatenate([np.load("vecs_0000000.npy", mmap_mode="r"), np.load("vecs_0050000.npy", mmap_mode="r")])
bucket = [zlib.crc32(p.encode()) % 1000 for p in ids]

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, timeout=120)
N = "products_100k"
if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=VectorParams(size=1024, distance=Distance.COSINE))
client.create_payload_index(N, "bucket", PayloadSchemaType.INTEGER)

for start in range(0, len(ids), 500):
    client.upsert(N, points=[PointStruct(id=i, vector=vectors[i].tolist(), payload={"bucket": bucket[i]})
                             for i in range(start, min(start + 500, len(ids)))])
print("넣은 상품", client.count(N).count)
