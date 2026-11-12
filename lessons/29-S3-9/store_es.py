import sys

from qdrant_client import QdrantClient

from embed import embed

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)


def search_es(text):
    return client.query_points("products_markets", query=embed(text), limit=5).points


for h in search_es(sys.argv[1]):
    print(h.payload["market"], "|", h.payload["title"][:40])
