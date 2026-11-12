import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

vecs = np.load("book_vecs.npy")
client = QdrantClient(url="http://localhost:6333")
points = [PointStruct(id=i, vector=vecs[i].tolist()) for i in range(len(vecs))]

for col, dist in [("books_cos", Distance.COSINE), ("books_euclid", Distance.EUCLID)]:
    if client.collection_exists(col):
        client.delete_collection(col)
    client.create_collection(collection_name=col, vectors_config=VectorParams(size=1024, distance=dist))
    client.upsert(collection_name=col, wait=True, points=points)

top_cos = [p.id for p in client.query_points("books_cos", query=vecs[0].tolist(), limit=10).points]
top_euc = [p.id for p in client.query_points("books_euclid", query=vecs[0].tolist(), limit=10).points]
print("Cosine 상위 10개 ID:", top_cos)
print("Euclid 상위 10개 ID:", top_euc)
print("순서가 완전히 같은가:", top_cos == top_euc)
