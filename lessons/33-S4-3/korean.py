from qdrant_client import QdrantClient

from bm25 import N, bm25_query, tokens, vocab
from embed import embed

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
PAIRS = [("air zoom pegasus 35 running shoe", "에어 줌 페가수스 35 러닝화"), ("crystal clear shower curtain", "투명한 샤워 커튼")]
for en, ko in PAIRS:
    for text in [en, ko]:
        print(f"[{text}] 토큰 {tokens(text)} → 사전에 있는 것 {[t for t in tokens(text) if t in vocab]}")
        sparse = client.query_points(N, query=bm25_query(text), using="bm25", limit=2).points
        dense = client.query_points("products", query=embed(text), limit=2).points
        print("  단어:", [h.payload["title"][:28] for h in sparse])
        print("  벡터:", [h.payload["title"][:28] for h in dense])
