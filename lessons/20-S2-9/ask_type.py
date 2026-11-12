import sys

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

from embed import embed

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
question = sys.argv[1] if len(sys.argv) > 1 else "My online store checkout is not working"
v = embed(question)


def ask(label, query_filter=None):
    hits = client.query_points("wix_full", query=v, query_filter=query_filter, limit=3, with_payload=["title", "article_type"]).points
    print(f"\n[{label}]")
    for h in hits:
        print(f"  {h.score:.3f} {h.payload['article_type']:16} {h.payload['title'][:60]}")


ask("전체")
ask("알려진 문제만", Filter(must=[FieldCondition(key="article_type", match=MatchValue(value="known_issue"))]))
