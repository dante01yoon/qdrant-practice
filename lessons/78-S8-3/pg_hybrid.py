import time

import numpy as np
import pandas as pd
import psycopg
from pgvector.psycopg import register_vector

from common import ndcg10, queries, query_vecs, rrf

products = pd.read_parquet("products.parquet")
vecs = np.load("product_vecs.npy")
conn = psycopg.connect("postgresql://postgres:course@localhost:5434/postgres", autocommit=True)
register_vector(conn)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS products_h")
cur.execute("CREATE TABLE products_h (product_id text PRIMARY KEY, embedding vector(1024), doc tsvector)")
with cur.copy("COPY products_h (product_id, embedding) FROM STDIN WITH (FORMAT BINARY)") as copy:
    copy.set_types(["text", "vector"])
    for r, v in zip(products.itertuples(), vecs):
        copy.write_row((r.product_id, v))
rows = [(" ".join(str(x) for x in [r.product_title, r.product_brand, r.product_color, str(r.product_bullet_point)[:600]] if x), r.product_id) for r in products.itertuples()]
cur.executemany("UPDATE products_h SET doc = to_tsvector('english', %s) WHERE product_id = %s", rows)
cur.execute("CREATE INDEX ON products_h USING hnsw (embedding vector_cosine_ops)")
cur.execute("CREATE INDEX ON products_h USING gin (doc)")
D = "SELECT product_id FROM products_h ORDER BY embedding <=> %s LIMIT {}"
T = "SELECT product_id FROM products_h, websearch_to_tsquery('english', %s) q WHERE doc @@ q ORDER BY ts_rank_cd(doc, q) DESC LIMIT {}"
TOR = "SELECT product_id FROM products_h, to_tsquery('english', %s) q WHERE doc @@ q ORDER BY ts_rank_cd(doc, q) DESC LIMIT {}"


def orq(text):
    words = [w for w in "".join(c if c.isalnum() else " " for c in text).split()]
    return " | ".join(words) or "x"


res = {"dense": [], "word and": [], "word or": [], "rrf": []}
ms = []
for i, q in enumerate(queries.itertuples()):
    d = [r[0] for r in cur.execute(D.format(50), (query_vecs[i],)).fetchall()]
    a = [r[0] for r in cur.execute(T.format(10), (q.query,)).fetchall()]
    t0 = time.perf_counter()
    o = [r[0] for r in cur.execute(TOR.format(50), (orq(q.query),)).fetchall()]
    ms.append((time.perf_counter() - t0) * 1000)
    res["dense"].append(ndcg10(q.query_id, d[:10]))
    res["word and"].append(ndcg10(q.query_id, a))
    res["word or"].append(ndcg10(q.query_id, o[:10]))
    res["rrf"].append(ndcg10(q.query_id, rrf([d, o])))
for k, v in res.items():
    print(f"{k:9} nDCG@10 {np.mean(v):.3f}")
print(f"단어 검색 시간 {np.median(ms):.1f}ms")
cur.execute("DROP TABLE products_h")
