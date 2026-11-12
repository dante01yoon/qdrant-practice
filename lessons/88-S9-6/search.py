import json
import os
import re

from qdrant_client import QdrantClient, models
from sentence_transformers import CrossEncoder, SentenceTransformer

client = QdrantClient(url=os.environ.get("QDRANT_URL", "http://localhost:6333"), grpc_port=int(os.environ.get("QDRANT_GRPC", "6334")), prefer_grpc=True)
model = SentenceTransformer("BAAI/bge-m3")
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=512)
vocabs = {"shop": json.load(open("shop_vocab.json")), "help": json.load(open("wix_vocab.json"))}
SURE = float(os.environ.get("SURE", "0.5"))


def sparse(text, vocab):
    ids = sorted({vocab[t] for t in re.findall(r"[a-z0-9]+", text.lower()) if t in vocab})
    return models.SparseVector(indices=ids, values=[1.0] * len(ids))


def hybrid(name, text, limit, flt=None):
    v = model.encode(text, normalize_embeddings=True).tolist()
    s = sparse(text, vocabs[name])
    if s.indices:
        args = dict(prefetch=[models.Prefetch(query=v, using="dense", limit=50), models.Prefetch(query=s, using="bm25", limit=50)],
                    query=models.FusionQuery(fusion=models.Fusion.DBSF))
    else:
        args = dict(query=v, using="dense")
    return client.query_points(name, limit=limit, query_filter=flt, **args).points


def search_products(q, brand="", color="", limit=10):
    must = [models.FieldCondition(key=k, match=models.MatchValue(value=x)) for k, x in [("product_brand", brand), ("product_color", color)] if x]
    hits = hybrid("shop", q, limit, models.Filter(must=must) if must else None)
    return [{"title": h.payload["title"], "brand": h.payload["product_brand"], "color": h.payload["product_color"],
             "url": "https://www.amazon.com/dp/" + h.payload["product_id"], "product_id": h.payload["product_id"]} for h in hits]


def ask_help(q, limit=5):
    hits = hybrid("help", q, 20)
    scores = reranker.predict([(q, h.payload["text"]) for h in hits])
    found, seen = [], set()
    for h, score in sorted(zip(hits, scores), key=lambda x: -x[1]):
        if h.payload["article_id"] not in seen:
            seen.add(h.payload["article_id"])
            found.append({"title": h.payload["title"], "url": h.payload["url"], "text": h.payload["text"], "article_id": h.payload["article_id"], "score": round(float(score), 3)})
    return {"sure": found[0]["score"] >= SURE, "found": found[:limit]}
