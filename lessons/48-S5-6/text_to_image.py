import shutil
import sys

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
english = SentenceTransformer("clip-ViT-B-32")
multilingual = SentenceTransformer("sentence-transformers/clip-ViT-B-32-multilingual-v1")


def search(model, text):
    hits = client.query_points("abo_images", query=model.encode(text, normalize_embeddings=True).tolist(), limit=3).points
    print(f"\n「{text}」")
    for k, h in enumerate(hits, 1):
        print(f"  {k}위 {h.score:.3f} {h.payload['type']:12} {h.payload['name'][:50]}")
        shutil.copy(f"small/{h.payload['image_id']}.jpg", f"top{k}.jpg")


search(english, "red office chair")
search(multilingual, "빨간 사무용 의자")
for text in sys.argv[1:]:
    search(multilingual, text)
