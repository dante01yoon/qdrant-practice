import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, IsEmptyCondition, MatchValue, PayloadField

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_final"


def point(product_id):
    return client.retrieve(N, ids=[str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{product_id}"))], with_vectors=True)[0]


print("① 개수:", client.count(N).count)

p = point("B08693FP1K")
print("② 칸과 모양:", {k: type(v).__name__ for k, v in sorted(p.payload.items())})
print("③ 벡터:", sorted(p.vector))

no_bullets = client.count(N, count_filter=Filter(must=[FieldCondition(key="bullet_count", match=MatchValue(value=0))])).count
print("④ 특징 없는 상품:", no_bullets, "개 · 그중 하나의 벡터:",
      sorted(client.scroll(N, scroll_filter=Filter(must=[FieldCondition(key="bullet_count", match=MatchValue(value=0))]), limit=1, with_vectors=True)[0][0].vector))

upper = client.count(N, count_filter=Filter(must=[FieldCondition(key="color", match=MatchValue(value="Black"))])).count
print("⑤ 대문자 Black:", upper, "· 소문자 black:", client.count(N, count_filter=Filter(must=[FieldCondition(key="color", match=MatchValue(value="black"))])).count)
print("⑥ 브랜드 칸 없는 상품:", client.count(N, count_filter=Filter(must=[IsEmptyCondition(is_empty=PayloadField(key="brand"))])).count)
