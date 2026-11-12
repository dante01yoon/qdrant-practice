import time

import numpy as np
import pandas as pd
import psycopg
from pgvector.psycopg import register_vector

from common import ndcg10, queries, query_vecs

products = pd.read_parquet("products.parquet").fillna("")
vecs = np.load("product_vecs.npy")
conn = psycopg.connect("postgresql://postgres:course@localhost:5434/postgres", autocommit=True, prepare_threshold=None)
conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
register_vector(conn)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS shop")
cur.execute("CREATE TABLE shop (product_id text PRIMARY KEY, title text, brand text, color text, embedding vector(1024))")
with cur.copy("COPY shop (product_id, title, brand, color, embedding) FROM STDIN WITH (FORMAT BINARY)") as copy:
    copy.set_types(["text", "text", "text", "text", "vector"])
    for r, v in zip(products.itertuples(), vecs):
        copy.write_row((r.product_id, r.product_title, r.product_brand, r.product_color, v))
cur.execute("CREATE INDEX ON shop USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 100)")
print("행", cur.execute("SELECT count(*) FROM shop").fetchone()[0])

SQL = "SELECT product_id, title FROM shop ORDER BY embedding <=> %s LIMIT 10"
for row in cur.execute(SQL, (query_vecs[0],)).fetchall()[:3]:
    print(row[0], row[1][:50])
print("검색어:", queries["query"].iloc[0])

scores, ms = [], []
for i, q in enumerate(queries.itertuples()):
    t = time.perf_counter()
    found = [r[0] for r in cur.execute(SQL, (query_vecs[i],)).fetchall()]
    ms.append((time.perf_counter() - t) * 1000)
    scores.append(ndcg10(q.query_id, found))
print(f"nDCG@10 {np.mean(scores):.3f} · 가운데 {np.median(ms):.1f}ms")
