import uuid

from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
pid = str(uuid.uuid5(uuid.NAMESPACE_URL, "amazon/B08693FP1K"))
print("개수:", client.count("products_load").count)
print("조리 도구 칸:", sorted(client.retrieve("products_load", ids=[pid])[0].payload))
