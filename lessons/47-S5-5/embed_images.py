import pandas as pd
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

items = pd.read_parquet("abo_photos.parquet")
model = SentenceTransformer("clip-ViT-B-32")

photos = [Image.open(f"small/{i}.jpg").convert("RGB") for i in items.image_id]
vectors = model.encode(photos, batch_size=64, normalize_embeddings=True, show_progress_bar=True)
print("사진", len(photos), "장 → 벡터", vectors.shape)

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
if client.collection_exists("abo_images"):
    client.delete_collection("abo_images")
client.create_collection("abo_images", vectors_config=VectorParams(size=512, distance=Distance.COSINE))
client.upload_points("abo_images", points=[
    PointStruct(id=k, vector=vectors[k].tolist(), payload={"name": r.name, "type": r.type, "image_id": r.image_id})
    for k, r in enumerate(items.itertuples())
], wait=True)
print("넣은 사진", client.count("abo_images").count)
