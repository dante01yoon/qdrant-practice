import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, MultiVectorComparator, MultiVectorConfig, PointStruct, VectorParams

client = QdrantClient(url="http://localhost:6333")
N = "toy_multi"
if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=VectorParams(size=3, distance=Distance.DOT,
                                                        multivector_config=MultiVectorConfig(comparator=MultiVectorComparator.MAX_SIM)))

doc = [[0.9, 0.1, 0.0], [0.1, 0.8, 0.1], [0.0, 0.2, 0.9]]
query = [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
client.upsert(N, points=[PointStruct(id=1, vector=doc)])


def maxsim(q, d):
    sims = np.array(q) @ np.array(d).T
    print("토큰끼리 내적 표:\n", sims.round(2))
    return sims.max(axis=1).sum()


print("손계산 MaxSim:", round(maxsim(query, doc), 2))
print("Qdrant 점수:", round(client.query_points(N, query=query).points[0].score, 2))

client.upsert(N, points=[PointStruct(id=2, vector=[[0.1, 0.2], [0.3, 0.4]])])
