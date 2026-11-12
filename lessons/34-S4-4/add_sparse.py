import uuid

import numpy as np
from qdrant_client.models import (Distance, Modifier, PointStruct, PointVectors, SparseVectorConfig, SparseVectorNameConfig,
                                  VectorParams)

from bm25 import bm25_doc, bm25_query, client, docs, products

N = "products_plus"
vecs = np.load("product_vecs.npy")
ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{p}")) for p in products["product_id"]]

if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config={"dense": VectorParams(size=1024, distance=Distance.COSINE)})
client.upload_points(N, points=[PointStruct(id=ids[i], vector={"dense": vecs[i].tolist()}, payload={"title": t})
                                for i, t in enumerate(products["product_title"])], batch_size=256, wait=True)
print("처음 벡터 이름:", list(client.get_collection(N).config.params.vectors), "· sparse:", client.get_collection(N).config.params.sparse_vectors)


client.create_vector_name(N, "bm25", SparseVectorNameConfig(sparse=SparseVectorConfig(modifier=Modifier.IDF)))
for start in range(0, len(ids), 500):
    client.update_vectors(N, points=[PointVectors(id=ids[i], vector={"bm25": bm25_doc(docs[i])})
                                     for i in range(start, min(start + 500, len(ids)))])
print("더한 뒤 sparse:", list(client.get_collection(N).config.params.sparse_vectors))


for h in client.query_points(N, query=bm25_query("eleven baby mask"), using="bm25", limit=2).points:
    print(f"  {h.score:.2f} {h.payload['title'][:45]}")
