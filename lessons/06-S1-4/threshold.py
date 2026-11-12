import time

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, OptimizersConfigDiff, PointStruct, VectorParams

client = QdrantClient(url="http://localhost:6333")
if client.collection_exists("products_threshold_1000"):
    client.delete_collection("products_threshold_1000")

client.create_collection(
    collection_name="products_threshold_1000",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    optimizers_config=OptimizersConfigDiff(indexing_threshold=1000),
)

vecs = np.load("product_vecs.npy")
for start in range(0, len(vecs), 500):
    batch = [PointStruct(id=i, vector=vecs[i].tolist()) for i in range(start, min(start + 500, len(vecs)))]
    client.upsert(collection_name="products_threshold_1000", points=batch)

for _ in range(30):
    info = client.get_collection(collection_name="products_threshold_1000")
    if info.indexed_vectors_count > 0:
        break
    time.sleep(1)

print("바뀐 인덱싱 기준값:", info.config.optimizer_config.indexing_threshold)
print("색인된 벡터 수:", info.indexed_vectors_count)
