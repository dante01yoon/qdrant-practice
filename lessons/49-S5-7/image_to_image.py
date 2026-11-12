import pandas as pd
from PIL import Image, ImageEnhance
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
model = SentenceTransformer("clip-ViT-B-32")
items = pd.read_parquet("abo_photos.parquet")

k = items.index[items.type == "CHAIR"][0]
photo = Image.open(f"small/{items.image_id[k]}.jpg").convert("RGB")
w, h = photo.size
variants = {
    "original": photo,
    "crop": photo.crop((int(w * 0.15), int(h * 0.15), int(w * 0.85), int(h * 0.85))),
    "dark": ImageEnhance.Brightness(photo).enhance(0.5),
    "gray": photo.convert("L").convert("RGB"),
}
print("찾을 사진:", items.name[k][:60])
for name, img in variants.items():
    img.save(f"{name}.jpg")
    hits = client.query_points("abo_images", query=model.encode(img, normalize_embeddings=True).tolist(), limit=3).points
    rank = next((j + 1 for j, hit in enumerate(hits) if hit.id == k), "-")
    print(f"{name:8} 자기 자신 {rank}위 · 1위 점수 {hits[0].score:.3f} · {[hit.payload['type'] for hit in hits]}")
