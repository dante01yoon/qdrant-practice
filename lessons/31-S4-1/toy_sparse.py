from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, SparseVector, SparseVectorParams

client = QdrantClient(url="http://localhost:6333")
N = "toy_sparse"

if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config={}, sparse_vectors_config={"words": SparseVectorParams()})

WORDS = {"silicone": 0, "spatula": 1, "steel": 2, "shower": 3, "curtain": 4, "clear": 5}


def sparse(text):
    ids = sorted({WORDS[w] for w in text.split() if w in WORDS})
    return SparseVector(indices=ids, values=[1.0] * len(ids))


for i, title in enumerate(["silicone spatula", "steel spatula", "clear shower curtain"], start=1):
    client.upsert(N, points=[PointStruct(id=i, vector={"words": sparse(title)}, payload={"title": title})])

for hit in client.query_points(N, query=sparse("silicone spatula"), using="words").points:
    print(hit.score, hit.payload["title"])

client.upsert(N, points=[PointStruct(id=9, vector={"words": SparseVector(indices=[0, 1], values=[1.0])})])
