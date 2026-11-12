# 섹션 4·9가 쓰는 wix_full 컬렉션: WixQA 글 전체를 800자 조각(100자 겹침)으로 나눠 bge-m3로 넣는다.
# S2-9 pipeline.py와 같은 방식이고 컬렉션 이름만 wix_full. CPU에서는 오래 걸린다(수십 분).
#   uv run python scripts/prepare_wixqa.py && uv run python scripts/build_wix_full.py
import json
import sys
import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

D = Path(__file__).resolve().parent.parent / "data"
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else None
model = SentenceTransformer("BAAI/bge-m3")
client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)


def chunk(text, size=800, overlap=100):
    pieces, start = [], 0
    while start < len(text):
        pieces.append(text[start:start + size])
        if start + size >= len(text):
            break
        start += size - overlap
    return pieces


with open(D / "wix_kb_corpus.jsonl", encoding="utf-8") as f:
    articles = [json.loads(line) for k, line in enumerate(f) if LIMIT is None or k < LIMIT]
records = [(str(uuid.uuid5(uuid.NAMESPACE_URL, f"wix/{a['id']}/{i}")), piece,
            {"article_id": a["id"], "title": a["title"], "url": a["url"], "article_type": a["article_type"], "chunk": i, "text": piece})
           for a in articles for i, piece in enumerate(chunk(a["contents"]))]
print("글:", len(articles), "/ 조각:", len(records))
if not client.collection_exists("wix_full"):
    client.create_collection("wix_full", vectors_config=VectorParams(size=1024, distance=Distance.COSINE))
for start in range(0, len(records), 128):
    part = records[start:start + 128]
    vecs = model.encode([t for _, t, _ in part], normalize_embeddings=True)
    client.upsert("wix_full", points=[PointStruct(id=pid, vector=v.tolist(), payload=p) for (pid, _, p), v in zip(part, vecs)])
print("컬렉션 점 개수:", client.count("wix_full").count)
