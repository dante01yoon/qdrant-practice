import time
import uuid

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


def main():
    products = pd.read_parquet("products.parquet").fillna("")
    vecs = np.load("product_vecs.npy")
    ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{p}")) for p in products["product_id"]]
    points = [PointStruct(id=ids[i], vector=vecs[i].tolist(), payload={"title": t}) for i, t in enumerate(products["product_title"])]
    for grpc, parallel in [(False, 1), (False, 4), (True, 1)]:
        client = QdrantClient(url="http://localhost:6333", prefer_grpc=grpc)
        if client.collection_exists("products_batch"):
            client.delete_collection("products_batch")
        client.create_collection("products_batch", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))
        t0 = time.perf_counter()
        client.upload_points("products_batch", points=points, batch_size=256, parallel=parallel, wait=True)
        print(f"{'gRPC' if grpc else 'REST'} · {parallel}개 동시: {time.perf_counter() - t0:.1f}초")


if __name__ == "__main__":
    main()
