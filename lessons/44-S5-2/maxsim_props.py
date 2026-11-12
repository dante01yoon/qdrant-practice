from qdrant_client import QdrantClient
from qdrant_client.models import Distance, MultiVectorComparator, MultiVectorConfig, PointStruct, VectorParams

client = QdrantClient(url="http://localhost:6333")
N = "toy_props"
if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=VectorParams(size=3, distance=Distance.DOT,
                                                        multivector_config=MultiVectorConfig(comparator=MultiVectorComparator.MAX_SIM)))

doc = [[0.9, 0.1, 0.0], [0.1, 0.8, 0.1], [0.0, 0.2, 0.9]]
query = [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
client.upsert(N, points=[
    PointStruct(id=1, vector=doc, payload={"name": "원래 글 · 토큰 3개"}),
    PointStruct(id=2, vector=doc[::-1], payload={"name": "순서만 뒤집음"}),
    PointStruct(id=3, vector=doc + [[0.3, 0.3, 0.3], [0.5, 0.0, 0.5]], payload={"name": "토큰 2개 더 붙임"}),
    PointStruct(id=4, vector=doc + [[1.0, 0.0, 0.0]], payload={"name": "검색어와 똑같은 토큰 하나 더"}),
])
for h in client.query_points(N, query=query, with_payload=True).points:
    print(f"{h.score:.2f} {h.payload['name']}")
