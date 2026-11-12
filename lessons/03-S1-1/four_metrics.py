from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

client = QdrantClient(url="http://localhost:6333")

points = [
    PointStruct(id=1, vector=[0.9, 0.1, 0.8, 0.0], payload={"name": "산 노을"}),
    PointStruct(id=2, vector=[0.1, 0.1, 0.9, 0.0], payload={"name": "바다 노을"}),
    PointStruct(id=3, vector=[0.2, 0.9, 0.1, 0.7], payload={"name": "도시 야경"}),
]
q = [0.8, 0.2, 0.9, 0.1]

metrics = {
    "dot": Distance.DOT,
    "cosine": Distance.COSINE,
    "euclid": Distance.EUCLID,
    "manhattan": Distance.MANHATTAN,
}

for name, dist in metrics.items():
    col = f"test_{name}"
    if client.collection_exists(col):
        client.delete_collection(col)
    client.create_collection(collection_name=col, vectors_config=VectorParams(size=4, distance=dist))
    client.upsert(collection_name=col, wait=True, points=points)
    res = client.query_points(collection_name=col, query=q, with_payload=True, limit=3).points
    print(name, [(p.id, p.payload["name"], round(p.score, 4)) for p in res])

res_vec = client.query_points(collection_name="test_cosine", query=q, with_vectors=True, limit=1).points[0]
print("원래 넣은 벡터:", [0.9, 0.1, 0.8, 0.0])
print("Cosine에서 꺼낸 벡터:", [round(x, 4) for x in res_vec.vector])
