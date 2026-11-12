import json
import re
from collections import Counter

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, Modifier, PointStruct, SparseVector, SparseVectorParams, VectorParams

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, timeout=60)


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


chunks, offset = [], None
while True:
    got, offset = client.scroll("wix_full", limit=2000, offset=offset, with_vectors=True, with_payload=True)
    chunks += got
    if offset is None:
        break
docs = [tokens(c.payload["text"]) for c in chunks]
print("조각", len(chunks))


vocab = {}
for doc in docs:
    for t in doc:
        vocab.setdefault(t, len(vocab))
json.dump(vocab, open("wix_vocab.json", "w"))
avg_len = sum(map(len, docs)) / len(docs)
print("사전 단어", len(vocab), "· 조각 평균 토큰", round(avg_len))


def bm25(doc, k1=1.2, b=0.75):
    tf = Counter(doc)
    norm = k1 * (1 - b + b * len(doc) / avg_len)
    return SparseVector(indices=[vocab[t] for t in tf], values=[f * (k1 + 1) / (f + norm) for f in tf.values()])


N = "wix_hybrid"
if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config={"dense": VectorParams(size=1024, distance=Distance.COSINE)},
                         sparse_vectors_config={"bm25": SparseVectorParams(modifier=Modifier.IDF)})
client.upload_points(N, points=[PointStruct(id=c.id, vector={"dense": c.vector, "bm25": bm25(d)}, payload=c.payload)
                                for c, d in zip(chunks, docs)], batch_size=256, wait=True)
print("넣은 조각", client.count(N).count)
