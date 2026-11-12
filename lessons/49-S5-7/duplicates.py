import numpy as np
import pandas as pd
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
items = pd.read_parquet("abo_photos.parquet")
points, _ = client.scroll("abo_images", limit=3000, with_vectors=True)
points.sort(key=lambda p: p.id)
vecs = np.array([p.vector for p in points])

sim = vecs @ vecs.T
i, j = np.triu_indices(len(vecs), k=1)
s = sim[i, j]
same_photo = items.image_id.values[i] == items.image_id.values[j]
print("상품 쌍", len(s), "개")
print("같은 사진 파일을 쓰는 쌍", same_photo.sum(), "· 점수 최소", round(s[same_photo].min(), 4))
near = (~same_photo) & (s > 0.95)
print("다른 사진인데 0.95 넘는 쌍", near.sum())
for a, b, v in sorted(zip(i[near], j[near], s[near]), key=lambda x: -x[2])[:3]:
    print(f"  {v:.3f} {items.name[a][:35]} | {items.name[b][:35]}")
