from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
english = SentenceTransformer("clip-ViT-B-32")
multilingual = SentenceTransformer("sentence-transformers/clip-ViT-B-32-multilingual-v1")


def top10(model, text, only=None):
    f = Filter(must=[FieldCondition(key="type", match=MatchValue(value=only))]) if only else None
    return client.query_points("abo_images", query=model.encode(text, normalize_embeddings=True).tolist(), query_filter=f, limit=10).points


for name, model, text in [("영어", english, "running shoes"), ("다국어", multilingual, "running shoes"), ("다국어", multilingual, "러닝화"),
                          ("다국어", multilingual, "운동화"), ("다국어", multilingual, "신발")]:
    types = [h.payload["type"] for h in top10(model, text)]
    print(f"{name:3} 「{text}」 위 10개 중 SHOES {types.count('SHOES')}개 · 1위 {types[0]}")

print("\n「러닝화」 + 종류 필터 SHOES")
for k, h in enumerate(top10(multilingual, "러닝화", only="SHOES")[:3], 1):
    print(f"  {k}위 {h.score:.3f} {h.payload['name'][:55]}")
