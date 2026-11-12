import json
import sys
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from embed import model

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else None
client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)


def read_articles(path, limit=None):
    with open(path, encoding="utf-8") as f:
        for k, line in enumerate(f):
            if limit is not None and k >= limit:
                break
            yield json.loads(line)


def chunk(text, size=800, overlap=100):
    pieces, start = [], 0
    while start < len(text):
        pieces.append(text[start:start + size])
        if start + size >= len(text):
            break
        start += size - overlap
    return pieces


def to_records(article):
    for i, piece in enumerate(chunk(article["contents"])):
        pid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"wix/{article['id']}/{i}"))
        payload = {"article_id": article["id"], "title": article["title"], "url": article["url"],
                   "article_type": article["article_type"], "chunk": i, "text": piece}
        yield pid, piece, payload


def load(records, batch=128):
    for start in range(0, len(records), batch):
        part = records[start:start + batch]
        vecs = model.encode([text for _, text, _ in part], normalize_embeddings=True)
        points = [PointStruct(id=pid, vector=v.tolist(), payload=p) for (pid, _, p), v in zip(part, vecs)]
        client.upsert("wix_chunks", points=points)


if not client.collection_exists("wix_chunks"):
    client.create_collection("wix_chunks", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))
articles = list(read_articles("wix_kb_corpus.jsonl", LIMIT))
records = [r for a in articles for r in to_records(a)]
print("글:", len(articles), "/ 조각:", len(records))
load(records)
print("컬렉션 점 개수:", client.count("wix_chunks").count)
