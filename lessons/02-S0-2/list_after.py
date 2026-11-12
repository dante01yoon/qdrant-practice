from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
names_after = [c.name for c in client.get_collections().collections]
print("컨테이너 다시 띄운 뒤 목록:", names_after)
