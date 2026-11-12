import time

import numpy as np
import psycopg
from pgvector.psycopg import register_vector

queries = np.load("query_vecs.npy")[:100]
conn = psycopg.connect("postgresql://postgres:course@localhost:5434/postgres", autocommit=True, prepare_threshold=None)
register_vector(conn)
cur = conn.cursor()
SQL = "SELECT id FROM products_100k ORDER BY embedding <=> %s LIMIT 10"

cur.execute("SET enable_indexscan = off")
truth = [{r[0] for r in cur.execute(SQL, (q,)).fetchall()} for q in queries]
cur.execute("SET enable_indexscan = on")

for ef in [128, 160, 200, 256]:
    cur.execute(f"SET hnsw.ef_search = {ef}")
    got, ms = [], []
    for q in queries:
        t = time.perf_counter()
        got.append({r[0] for r in cur.execute(SQL, (q,)).fetchall()})
        ms.append((time.perf_counter() - t) * 1000)
    recall = np.mean([len(g & w) / 10 for g, w in zip(got, truth)])
    print(f"ef_search {ef:3} · recall@10 {recall:.3f} · {np.median(ms):.1f}ms" + (" ← 0.95 넘음" if recall >= 0.95 else ""))
