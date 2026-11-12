import numpy as np
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")
N = "market_products"
vec = np.load("query_vecs.npy")[0].tolist()


def only(market):
    return models.Filter(must=[models.FieldCondition(key="market", match=models.MatchValue(value=market))])


def show(title, flt):
    hits = client.query_points(N, query=vec, query_filter=flt, limit=3, with_payload=True).points
    print(title)
    for h in hits:
        print(f"  {h.score:.3f} {h.payload['market']} {h.payload['title'][:40]}")


show("필터 없음", None)
show("us만", only("us"))
show("es만", only("es"))
show("jp만", only("jp"))
