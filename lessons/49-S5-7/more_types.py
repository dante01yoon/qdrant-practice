import pandas as pd
from PIL import Image
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
model = SentenceTransformer("clip-ViT-B-32")
items = pd.read_parquet("abo_photos.parquet")

for t in ["SHOES", "RUG", "LAMP", "SOFA"]:
    k = items.index[items.type == t][0]
    photo = Image.open(f"small/{items.image_id[k]}.jpg").convert("RGB")
    hits = client.query_points("abo_images", query=model.encode(photo, normalize_embeddings=True).tolist(), limit=6).points
    others = [h.payload["type"] for h in hits if h.id != k][:5]
    print(f"{t:8} 자기 자신 {next(j + 1 for j, h in enumerate(hits) if h.id == k)}위 · 나머지 5개 중 같은 종류 {others.count(t)}개 · {others}")
