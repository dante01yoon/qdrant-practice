import threading
import time

import numpy as np
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333", timeout=60)
queries = np.load("query_vecs.npy")[:200]
counts = {"성공": 0, "실패": 0}
running = True


def traffic():
    i = 0
    while running:
        try:
            client.query_points("products_live", query=queries[i % 200].tolist(), limit=1)
            counts["성공"] += 1
        except Exception:
            counts["실패"] += 1
        i += 1


def point_to(old, new):
    client.update_collection_aliases(change_aliases_operations=[
        models.DeleteAliasOperation(delete_alias=models.DeleteAlias(alias_name="products_live")),
        models.CreateAliasOperation(create_alias=models.CreateAlias(collection_name=new, alias_name="products_live"))])
    print(old, "→", new)


t = threading.Thread(target=traffic)
t.start()
time.sleep(3)
point_to("products_v1", "products_v2")
time.sleep(3)
point_to("products_v2", "products_v1")
time.sleep(3)
running = False
t.join()
print(counts)
