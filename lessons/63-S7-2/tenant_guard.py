import numpy as np
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")
N = "market_products"
MARKETS = {"us", "es", "jp"}
vec = np.load("query_vecs.npy")[0].tolist()


def search(market, vector, limit=3):
    if market not in MARKETS:
        raise ValueError(f"모르는 마켓: {market}")
    only = models.Filter(must=[models.FieldCondition(key="market", match=models.MatchValue(value=market))])
    return client.query_points(N, query=vector, query_filter=only, limit=limit, with_payload=True).points


for market in ["jp", "kr", None]:
    try:
        print(market, "→", [h.payload["market"] for h in search(market, vec)])
    except ValueError as e:
        print(market, "→ 막음:", e)
