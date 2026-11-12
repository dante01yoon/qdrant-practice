from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

from embed import embed

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
MARKETS = {"us", "es", "jp"}


def search(text, market, limit=5):
    if market not in MARKETS:
        raise ValueError(f"모르는 마켓: {market}")
    only = Filter(must=[FieldCondition(key="market", match=MatchValue(value=market))])
    return client.query_points("products_markets", query=embed(text), query_filter=only, limit=limit).points


if __name__ == "__main__":
    for text, market in [("zapatillas running mujer", "es"), ("大きいスリッパ メンズ", "jp")]:
        hits = search(text, market)
        assert all(h.payload["market"] == market for h in hits), "다른 마켓 상품이 섞였어요"
        print(text, market, [h.payload["title"][:20] for h in hits[:3]])
    print("검사 통과 · 모든 결과가 요청한 마켓")
