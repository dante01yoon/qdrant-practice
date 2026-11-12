import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, Fusion, FusionQuery, MatchValue, Prefetch
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
model = SentenceTransformer("sentence-transformers/clip-ViT-B-32-multilingual-v1")
N = "abo_mixed"


def search(text, way, only):
    v = model.encode(text, normalize_embeddings=True).tolist()
    f = Filter(must=[FieldCondition(key="type", match=MatchValue(value=only))]) if only else None
    if way == "mix":
        args = dict(prefetch=[Prefetch(query=v, using="photo", limit=30), Prefetch(query=v, using="name", limit=30)],
                    query=FusionQuery(fusion=Fusion.RRF))
    else:
        args = dict(query=v, using=way)
    return [h.payload for h in client.query_points(N, limit=8, query_filter=f, **args).points]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/search":
            q = parse_qs(url.query)
            body, kind = json.dumps(search(q["q"][0], q["way"][0], q.get("only", [""])[0])).encode(), "application/json"
        elif url.path.startswith("/small/"):
            body, kind = (Path("small") / Path(url.path).name).read_bytes(), "image/jpeg"
        else:
            body, kind = Path("index.html").read_bytes(), "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.end_headers()
        self.wfile.write(body)


print("http://localhost:8000 에서 열어 보세요")
HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
