import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, Range

client = QdrantClient(url="http://localhost:6333")
N = "products_final"
count = lambda f: client.count(N, count_filter=f).count

black = FieldCondition(key="color", match=MatchValue(value="black"))
white = FieldCondition(key="color", match=MatchValue(value="white"))
five = FieldCondition(key="bullet_count", range=Range(gte=5))

print("black:", count(Filter(must=[black])), "/ white:", count(Filter(must=[white])))
print("must [black, white]:", count(Filter(must=[black, white])))
print("should [black, white]:", count(Filter(should=[black, white])))
print("must [five] + should [black, white]:", count(Filter(must=[five], should=[black, white])))
print("must_not [black]:", count(Filter(must_not=[black])))

queries = pd.read_csv("queries.csv")
row = queries.index[queries["query"] == "non metal cooking utensils"][0]
query_vec = np.load("query_vecs.npy")[row].tolist()
hits = client.query_points(N, query=query_vec, using="all", query_filter=Filter(must=[black, five]), limit=3,
                           with_payload=["title", "color", "bullet_count"]).points
for h in hits:
    print(round(h.score, 3), h.payload["color"], h.payload["bullet_count"], h.payload["title"][:30])
