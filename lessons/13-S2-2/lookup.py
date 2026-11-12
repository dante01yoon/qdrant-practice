import uuid

from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")


def point_id(product_id):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{product_id}"))


wanted = ["B08693FP1K", "B000000000"]
found = client.retrieve("products_uuid", ids=[point_id(p) for p in wanted], with_payload=True)
print("찾은 점:", len(found))
for p in found:
    print(p.id, p.payload["product_id"], p.payload["title"][:50])
