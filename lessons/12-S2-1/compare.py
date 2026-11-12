from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")

if client.collection_exists("products_euclid"):
    client.delete_collection("products_euclid")
client.create_collection("products_euclid", vectors_config=VectorParams(size=1024, distance=Distance.EUCLID))


def show(name):
    cfg = client.get_collection(name).config
    v = cfg.params.vectors
    print(f"{name:16} | {v.size} | {v.distance.value:9} | m={cfg.hnsw_config.m} | 기준값={cfg.optimizer_config.indexing_threshold}")

for name in ["products_v2", "products_euclid"]:
    show(name)
