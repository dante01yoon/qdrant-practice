import os
import sys

sys.path.insert(0, os.getcwd())  # 수업 폴더의 bm25.py를 불러오려고(수업 폴더에서 실행)
import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, Modifier, PointStruct, SparseVectorParams, VectorParams

from bm25 import bm25_doc, docs

products = pd.read_parquet("products.parquet")
vecs = np.load("product_vecs.npy")
client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_hybrid"

if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(
    N,
    vectors_config={"dense": VectorParams(size=1024, distance=Distance.COSINE)},
    sparse_vectors_config={"bm25": SparseVectorParams(modifier=Modifier.IDF)},
)

points = [
    PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{r.product_id}")),
                vector={"dense": vecs[i].tolist(), "bm25": bm25_doc(docs[i])},
                payload={"product_id": r.product_id, "title": r.product_title})
    for i, r in enumerate(products.itertuples())
]
client.upload_points(N, points=points, batch_size=256, wait=True)

p = client.retrieve(N, ids=[points[0].id], with_vectors=True)[0]
print("개수:", client.count(N).count)
print("dense 칸:", len(p.vector["dense"]), "/ bm25 칸(0이 아닌 것):", len(p.vector["bm25"].indices))
