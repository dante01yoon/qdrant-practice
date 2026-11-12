import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

client = QdrantClient(url="http://localhost:6333")
pid = str(uuid.uuid5(uuid.NAMESPACE_URL, "amazon/B08693FP1K"))

before = client.retrieve("products_load", ids=[pid], with_vectors=True)[0]
print("바꾸기 전 칸:", sorted(before.payload))

client.upsert("products_load", points=[PointStruct(id=pid, vector=before.vector, payload={"title": "Kitchen Utensil Set (상품명 고침)"})])
after = client.retrieve("products_load", ids=[pid])[0]
print("바꾼 뒤 칸:", sorted(after.payload))
