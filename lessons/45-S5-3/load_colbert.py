import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, HnswConfigDiff, MultiVectorComparator, MultiVectorConfig, PointStruct, VectorParams

products = pd.read_parquet("products.parquet")
dense = np.load("product_vecs.npy", mmap_mode="r")
tokens = np.load("colbert_tokens.npy", mmap_mode="r")
lens = np.load("colbert_lens.npy")
starts = np.concatenate([[0], np.cumsum(lens)])

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, timeout=120)
N = "products_colbert"
if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config={
    "dense": VectorParams(size=1024, distance=Distance.COSINE),
    "colbert": VectorParams(size=96, distance=Distance.COSINE,
                            multivector_config=MultiVectorConfig(comparator=MultiVectorComparator.MAX_SIM),
                            hnsw_config=HnswConfigDiff(m=0)),
})


def point(i, row):
    return PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{row.product_id}")),
                       vector={"dense": dense[i].tolist(), "colbert": tokens[starts[i]:starts[i + 1]].tolist()},
                       payload={"product_id": row.product_id})


client.upload_points(N, points=(point(i, r) for i, r in enumerate(products.itertuples())), batch_size=64, wait=True)
print("넣은 상품", client.count(N).count, "· 토큰 벡터", int(lens.sum()))
