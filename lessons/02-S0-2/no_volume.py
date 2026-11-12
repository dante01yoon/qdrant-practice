from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="demo",
    vectors_config=VectorParams(size=4, distance=Distance.COSINE),
)

names = [c.name for c in client.get_collections().collections]
print("컨테이너 재시작 전 목록:", names)
