from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, Range

from embed import embed

client = QdrantClient(url="http://localhost:6333")
N = "products_final"


def build_filter(brand=None, color=None, min_bullets=None):
    must = []
    if brand:
        must.append(FieldCondition(key="brand", match=MatchValue(value=brand)))
    if color:
        must.append(FieldCondition(key="color", match=MatchValue(value=color.strip().lower())))
    if min_bullets is not None:
        must.append(FieldCondition(key="bullet_count", range=Range(gte=min_bullets)))
    return Filter(must=must) if must else None


def search_products(text, limit=5, threshold=0.5, **conditions):
    hits = client.query_points(N, query=embed(text), using="all", query_filter=build_filter(**conditions),
                               limit=limit, score_threshold=threshold, with_payload=["title", "brand", "color"]).points
    if not hits:
        print(f"[{text} | {conditions}] 결과 없음 · 조건을 줄여 보세요")
    for h in hits:
        p = h.payload
        print(f"  {h.score:.3f} | {p.get('brand')} | {p.get('color')} | {p['title'][:30]}")
    return hits


if __name__ == "__main__":
    search_products("non metal cooking utensils", color=" Black ")
    search_products("non metal cooking utensils", color="black", min_bullets=5, limit=3)
    search_products("running shoes", brand="Nike", limit=3)
    search_products("running shoes", brand="Nike", color="purple")
