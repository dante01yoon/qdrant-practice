from qdrant_client import QdrantClient
from qdrant_client.models import Distance, Fusion, FusionQuery, PointStruct, Prefetch, VectorParams

client = QdrantClient(url="http://localhost:6333")
if client.collection_exists("hybrid_preview"):
    client.delete_collection("hybrid_preview")
client.create_collection(
    collection_name="hybrid_preview",
    vectors_config={
        "dense_a": VectorParams(size=4, distance=Distance.COSINE),
        "dense_b": VectorParams(size=4, distance=Distance.COSINE),
    },
)

client.upsert(
    collection_name="hybrid_preview",
    wait=True,
    points=[
        PointStruct(id=1, vector={"dense_a": [0.9, 0.1, 0.8, 0.0], "dense_b": [0.1, 0.9, 0.2, 0.8]}),
        PointStruct(id=2, vector={"dense_a": [0.1, 0.1, 0.9, 0.0], "dense_b": [0.8, 0.2, 0.9, 0.1]}),
    ],
)

res = client.query_points(
    collection_name="hybrid_preview",
    prefetch=[
        Prefetch(query=[0.8, 0.2, 0.9, 0.1], using="dense_a", limit=5),
        Prefetch(query=[0.8, 0.2, 0.9, 0.1], using="dense_b", limit=5),
    ],
    query=FusionQuery(fusion=Fusion.RRF),
    limit=2,
).points
print("RRF 결합 결과:", [(p.id, round(p.score, 4)) for p in res])
