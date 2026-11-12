import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, IsEmptyCondition, MatchAny, MatchExcept, MatchValue, PayloadField, Range

client = QdrantClient(url="http://localhost:6333")
N = "products_final"
count = lambda f: client.count(N, count_filter=f).count

print("특징 3~4개:", count(Filter(must=[FieldCondition(key="bullet_count", range=Range(gte=3, lte=4))])))
print("black 또는 white:", count(Filter(must=[FieldCondition(key="color", match=MatchAny(any=["black", "white"]))])))

black = FieldCondition(key="color", match=MatchValue(value="black"))
print("must_not black:", count(Filter(must_not=[black])))
print("MatchExcept black:", count(Filter(must=[FieldCondition(key="color", match=MatchExcept(**{"except": ["black"]}))])))
print("색상 비어 있음:", count(Filter(must=[IsEmptyCondition(is_empty=PayloadField(key="color"))])))
