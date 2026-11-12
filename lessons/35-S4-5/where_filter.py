import numpy as np
import pandas as pd
from qdrant_client.models import FieldCondition, Filter, Fusion, FusionQuery, MatchText, Prefetch

from bm25 import bm25_query, client

N = "products_hybrid"
text = "non metal cooking utensils"
queries = pd.read_csv("queries.csv")
vec = np.load("query_vecs.npy")[queries.index[queries["query"] == text][0]].tolist()
silicone = Filter(must=[FieldCondition(key="title", match=MatchText(text="silicone"))])


def show(label, **args):
    hits = client.query_points(N, query=FusionQuery(fusion=Fusion.RRF), limit=5, with_payload=["title"], **args).points
    print(f"\n[{label}] {len(hits)}개")
    for h in hits:
        print(f"  {h.score:.3f} silicone {'있음' if 'silicone' in h.payload['title'].lower() else '없음'} · {h.payload['title'][:40]}")


show("바깥 query_filter", prefetch=[Prefetch(query=vec, using="dense", limit=10), Prefetch(query=bm25_query(text), using="bm25", limit=10)],
     query_filter=silicone)
show("dense 쪽에만 filter", prefetch=[Prefetch(query=vec, using="dense", limit=10, filter=silicone), Prefetch(query=bm25_query(text), using="bm25", limit=10)])
