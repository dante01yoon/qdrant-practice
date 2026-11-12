from qdrant_client import QdrantClient

from embed import embed

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
question = "Can I start accepting payments on my site while my Wix Payments account is still under verification?"
for hit in client.query_points("wix_full", query=embed(question), limit=3).points:
    p = hit.payload
    print(f"{hit.score:.3f} | {p['title'][:45]} | 조각 {p['chunk']}")
