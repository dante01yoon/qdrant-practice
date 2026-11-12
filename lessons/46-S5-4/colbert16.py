import subprocess
import time
import uuid

import numpy as np
import pandas as pd
from qdrant_client.models import (Datatype, Distance, HnswConfigDiff, MultiVectorComparator, MultiVectorConfig,
                                  PointStruct, Prefetch, VectorParams)

from fusion_eval import client, ndcg10, queries, query_vecs

products = pd.read_parquet("products.parquet")
dense = np.load("product_vecs.npy", mmap_mode="r")
tokens = np.load("colbert_tokens.npy", mmap_mode="r")
starts = np.concatenate([[0], np.cumsum(np.load("colbert_lens.npy"))])
q_tokens = np.load("colbert_q_tokens.npy")
q_starts = np.concatenate([[0], np.cumsum(np.load("colbert_q_lens.npy"))])
N = "products_colbert16"
disk = lambda name: subprocess.run(["docker", "exec", "qdrant-course", "du", "-sh", f"/qdrant/storage/collections/{name}"], capture_output=True, text=True).stdout.split()[0]


if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config={
    "dense": VectorParams(size=1024, distance=Distance.COSINE),
    "colbert": VectorParams(size=96, distance=Distance.COSINE, datatype=Datatype.FLOAT16,
                            multivector_config=MultiVectorConfig(comparator=MultiVectorComparator.MAX_SIM),
                            hnsw_config=HnswConfigDiff(m=0)),
})
client.upload_points(N, points=(PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{r.product_id}")),
                                            vector={"dense": dense[i].tolist(), "colbert": tokens[starts[i]:starts[i + 1]].tolist()},
                                            payload={"product_id": r.product_id})
                                for i, r in enumerate(products.itertuples())), batch_size=64, wait=True)
print("넣은 직후 디스크", disk(N))
time.sleep(10)
print("10초 뒤 디스크", disk(N))


for name in ["products_colbert", N]:
    scores = []
    for i, q in enumerate(queries.itertuples()):
        hits = client.query_points(name, prefetch=[Prefetch(query=query_vecs[i].tolist(), using="dense", limit=50)],
                                   query=q_tokens[q_starts[i]:q_starts[i + 1]].tolist(), using="colbert", limit=10, with_payload=["product_id"]).points
        scores.append(ndcg10(q.query_id, [h.payload["product_id"] for h in hits]))
    print(f"{name:20} 디스크 {disk(name)} · nDCG@10 {np.mean(scores):.3f}")
