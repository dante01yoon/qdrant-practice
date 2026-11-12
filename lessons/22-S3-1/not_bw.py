from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, Range

client = QdrantClient(url="http://localhost:6333")
N = "products_final"
count = lambda f: client.count(N, count_filter=f).count
black = FieldCondition(key="color", match=MatchValue(value="black"))
white = FieldCondition(key="color", match=MatchValue(value="white"))

print("① must_not에 둘 다:", count(Filter(must_not=[black, white])))
print("② 「검정 또는 흰색」이 아닌 것:", count(Filter(must_not=[Filter(should=[black, white])])))

five_plus = FieldCondition(key="bullet_count", range=Range(gte=5))
print("③ (검정 또는 흰색) 그리고 특징 5개 이상:", count(Filter(must=[Filter(should=[black, white]), five_plus])))
print("   검정 또는 흰색만:", count(Filter(should=[black, white])), "/ 특징 5개 이상만:", count(Filter(must=[five_plus])))
