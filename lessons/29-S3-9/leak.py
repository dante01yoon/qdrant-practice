import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

from embed import embed

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_markets"
queries = pd.read_csv("market_qrels.csv")[["query", "product_locale"]].drop_duplicates()

for market, group in queries.groupby("product_locale"):
    leaked = total = 0
    for q in group["query"]:
        hits = client.query_points(N, query=embed(q), limit=5, with_payload=["market"]).points
        leaked += sum(h.payload["market"] != market for h in hits)
        total += len(hits)
    print(f"{market} 검색어 {len(group)}개 · 마켓 조건 없이 상위 5개 중 다른 나라 상품 {leaked}/{total} = {leaked / total:.0%}")

print("--- 마켓 필터를 걸면")
for market, group in queries.groupby("product_locale"):
    only = Filter(must=[FieldCondition(key="market", match=MatchValue(value=market))])
    leaked = sum(h.payload["market"] != market
                 for q in group["query"] for h in client.query_points(N, query=embed(q), query_filter=only, limit=5, with_payload=["market"]).points)
    print(f"{market} 다른 나라 상품 {leaked}개")
