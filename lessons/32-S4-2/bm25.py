import re
import uuid
from collections import Counter

import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Modifier, PointStruct, SparseVector, SparseVectorParams

products = pd.read_parquet("products.parquet").fillna("")
client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_bm25"


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


docs = [tokens(" ".join([r.product_title, r.product_brand, r.product_color, r.product_bullet_point[:600]])) for r in products.itertuples()]
vocab = {}
for d in docs:
    for t in d:
        vocab.setdefault(t, len(vocab))
avg_len = sum(len(d) for d in docs) / len(docs)


def bm25_doc(toks, k1=1.2, b=0.75):
    tf = Counter(toks)
    norm = k1 * (1 - b + b * len(toks) / avg_len)
    return SparseVector(indices=[vocab[t] for t in tf], values=[f * (k1 + 1) / (f + norm) for f in tf.values()])


def bm25_query(text):
    ids = sorted({vocab[t] for t in tokens(text) if t in vocab})
    return SparseVector(indices=ids, values=[1.0] * len(ids))


if not client.collection_exists(N):
    client.create_collection(N, vectors_config={}, sparse_vectors_config={"bm25": SparseVectorParams(modifier=Modifier.IDF)})
    points = [PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"amazon/{r.product_id}")), vector={"bm25": bm25_doc(d)},
                          payload={"product_id": r.product_id, "title": r.product_title}) for r, d in zip(products.itertuples(), docs)]
    client.upload_points(N, points=points, batch_size=256, wait=True)


if __name__ == "__main__":
    print("단어 사전:", len(vocab), "개 / 상품 글 평균 길이:", round(avg_len), "단어")
    for text in ["eleven baby mask", "non metal cooking utensils"]:
        print(text)
        for h in client.query_points(N, query=bm25_query(text), using="bm25", limit=3).points:
            print(f"  {h.score:.2f} {h.payload['title'][:40]}")
