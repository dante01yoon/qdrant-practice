from qdrant_client.models import Distance, VectorParams

print("지원하는 거리 방식:", [d.value for d in Distance])

params = VectorParams(size=1024, distance=Distance.COSINE)
print("벡터 설정 확인:", params)
