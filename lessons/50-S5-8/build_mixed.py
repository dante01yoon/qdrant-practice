import pandas as pd
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

items = pd.read_parquet("abo_photos.parquet")
clip = SentenceTransformer("clip-ViT-B-32")
multilingual = SentenceTransformer("sentence-transformers/clip-ViT-B-32-multilingual-v1")

photos = clip.encode([Image.open(f"small/{i}.jpg").convert("RGB") for i in items.image_id], batch_size=64, normalize_embeddings=True)
names = multilingual.encode(items.name.tolist(), batch_size=64, normalize_embeddings=True)

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "abo_mixed"
if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config={"photo": VectorParams(size=512, distance=Distance.COSINE),
                                            "name": VectorParams(size=512, distance=Distance.COSINE)})
client.upload_points(N, points=[
    PointStruct(id=k, vector={"photo": photos[k].tolist(), "name": names[k].tolist()},
                payload={"name": r.name, "type": r.type, "image_id": r.image_id})
    for k, r in enumerate(items.itertuples())
], wait=True)
print("넣은 상품", client.count(N).count)
