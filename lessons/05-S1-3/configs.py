from qdrant_client.models import Distance, VectorParams

configs = {
    "내적": VectorParams(size=4, distance=Distance.DOT),
    "코사인": VectorParams(size=4, distance=Distance.COSINE),
    "유클리드": VectorParams(size=4, distance=Distance.EUCLID),
    "맨해튼": VectorParams(size=4, distance=Distance.MANHATTAN),
}

for label, cfg in configs.items():
    print(f"{label} -> 차원: {cfg.size}, 거리: {cfg.distance.value}")
