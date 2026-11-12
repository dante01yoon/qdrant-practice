import numpy as np
import requests
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6401", timeout=120)
N = "products_cluster"
vecs = np.load("product_vecs.npy", mmap_mode="r")

if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE), shard_number=6, replication_factor=2)
client.upload_collection(N, vectors=vecs, ids=range(len(vecs)), batch_size=256, wait=True)

total = 0
for port in [6401, 6402, 6403]:
    info = requests.get(f"http://localhost:{port}/collections/{N}/cluster").json()["result"]
    print(port, [s["shard_id"] for s in info["local_shards"]], "점", sum(s["points_count"] for s in info["local_shards"]))
    total += sum(s["points_count"] for s in info["local_shards"])
print("모든 노드의 점을 더하면", total, "· 컬렉션의 점", client.count(N, exact=True).count)
