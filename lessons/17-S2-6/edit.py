import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, FilterSelector, MatchValue

client = QdrantClient(url="http://localhost:6333")
N = "products_load"
pid = str(uuid.uuid5(uuid.NAMESPACE_URL, "amazon/B08693FP1K"))


def show(step):
    p = client.retrieve(N, ids=[pid])[0].payload
    print(step, {k: (v[:20] if isinstance(v, str) else v) for k, v in sorted(p.items())})


show("처음")
client.set_payload(N, payload={"color": "black"}, points=[pid])
show("set_payload")
client.overwrite_payload(N, payload={"title": "Kitchen Utensil Set"}, points=[pid])
show("overwrite_payload")
client.set_payload(N, payload={"brand": "KITCHEN KRAFTERS", "product_id": "B08693FP1K", "color": "black"}, points=[pid])
client.delete_payload(N, keys=["color"], points=[pid])
show("delete_payload")
client.clear_payload(N, points_selector=[pid])
show("clear_payload")

feng = Filter(must=[FieldCondition(key="brand", match=MatchValue(value="Feng"))])
print("Feng 상품:", client.count(N, count_filter=feng).count)
client.delete(N, points_selector=FilterSelector(filter=feng))
print("지운 뒤 전체:", client.count(N).count, "/ Feng:", client.count(N, count_filter=feng).count)
