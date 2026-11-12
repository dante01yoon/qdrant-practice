import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import DenseVectorConfig, DenseVectorNameConfig, Distance, PointVectors

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_named"
products = pd.read_parquet("products.parquet")
vecs = np.load("product_vecs.npy")


client.create_vector_name(N, "all", DenseVectorNameConfig(dense=DenseVectorConfig(size=1024, distance=Distance.COSINE)))
print("벡터 이름:", sorted(client.get_collection(N).config.params.vectors))


for start in range(0, len(products), 500):
    batch = products.iloc[start:start + 500]
    client.update_vectors(N, points=[
        PointVectors(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{r.product_id}")), vector={"all": vecs[i].tolist()})
        for i, r in enumerate(batch.itertuples(), start=start)
    ])
p = client.retrieve(N, ids=[str(uuid.uuid5(uuid.NAMESPACE_URL, "amazon/B08693FP1K"))], with_vectors=True)[0]
print("점 개수:", client.count(N).count, "· 한 상품의 벡터:", sorted(p.vector))
