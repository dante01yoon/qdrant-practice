import numpy as np
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333", timeout=300)


def build(name, path):
    vecs = np.load(path)
    if client.collection_exists(name):
        client.delete_collection(name)
    client.create_collection(name, vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE))
    client.upload_collection(name, vectors=vecs, ids=range(len(vecs)), batch_size=500, wait=True)
    print(name, client.count(name, exact=True).count)


build("products_v1", "product_vecs.npy")
build("products_v2", "title_vecs.npy")

client.update_collection_aliases(change_aliases_operations=[
    models.CreateAliasOperation(create_alias=models.CreateAlias(collection_name="products_v1", alias_name="products_live"))])
print([(a.alias_name, a.collection_name) for a in client.get_aliases().aliases])

vec = np.load("query_vecs.npy")[0].tolist()
print("검색", [p.id for p in client.query_points("products_live", query=vec, limit=3).points])
