import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import RecommendInput, RecommendQuery

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
items = pd.read_parquet("abo_photos.parquet")
chair = int(items.index[items.type == "CHAIR"][0])
ottoman = int(items.index[items.type == "OTTOMAN"][0])
print("좋아요:", items.name[chair][:50])
print("싫어요:", items.name[ottoman][:50])


def show(title, query):
    hits = client.query_points("abo_images", query=query, limit=5).points
    print(f"\n{title}")
    for h in hits:
        print(f"  {h.score:.3f} {h.payload['type']:10} {h.payload['name'][:45]}")


show("좋아요 하나", RecommendQuery(recommend=RecommendInput(positive=[chair])))
show("좋아요 + 싫어요", RecommendQuery(recommend=RecommendInput(positive=[chair], negative=[ottoman])))
