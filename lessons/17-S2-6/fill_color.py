from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, IsEmptyCondition, MatchValue, PayloadField

client = QdrantClient(url="http://localhost:6333")
N = "products_load"

no_color = Filter(must=[IsEmptyCondition(is_empty=PayloadField(key="color"))])
print("색상 없는 상품:", client.count(N, count_filter=no_color).count)

client.set_payload(N, payload={"color": "unknown"}, points=no_color, wait=True)

unknown = Filter(must=[FieldCondition(key="color", match=MatchValue(value="unknown"))])
print("unknown:", client.count(N, count_filter=unknown).count, "/ 색상 없는 상품:", client.count(N, count_filter=no_color).count)
