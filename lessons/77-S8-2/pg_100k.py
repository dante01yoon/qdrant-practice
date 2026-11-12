import time

import numpy as np
import psycopg
from pgvector.psycopg import register_vector

vecs = np.load("vecs_100k.npy", mmap_mode="r")
queries = np.load("query_vecs.npy")[:200]
conn = psycopg.connect("postgresql://postgres:course@localhost:5434/postgres", autocommit=True, prepare_threshold=None)
conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
register_vector(conn)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS products_100k")
cur.execute("CREATE TABLE products_100k (id bigint PRIMARY KEY, embedding vector(1024))")
t0 = time.perf_counter()
with cur.copy("COPY products_100k (id, embedding) FROM STDIN WITH (FORMAT BINARY)") as copy:
    copy.set_types(["int8", "vector"])
    for i, v in enumerate(vecs):
        copy.write_row((i, v))
print(f"넣기 {time.perf_counter() - t0:.0f}초")

t0 = time.perf_counter()
cur.execute("SET maintenance_work_mem = '1GB'")
cur.execute("CREATE INDEX ON products_100k USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 100)")
print(f"색인 {time.perf_counter() - t0:.0f}초")
print("표+색인", cur.execute("SELECT pg_size_pretty(pg_total_relation_size('products_100k')), pg_size_pretty(pg_indexes_size('products_100k'))").fetchone())

SQL = "SELECT id FROM products_100k ORDER BY embedding <=> %s LIMIT 10"
cur.execute("SET enable_indexscan = off")
truth = [{r[0] for r in cur.execute(SQL, (q,)).fetchall()} for q in queries]
cur.execute("SET enable_indexscan = on")
print(cur.execute("EXPLAIN " + SQL, (queries[0],)).fetchall()[1][0].strip()[:70])
for ef in [16, 40, 64, 128, 256]:
    cur.execute(f"SET hnsw.ef_search = {ef}")
    got, ms = [], []
    for q in queries:
        t0 = time.perf_counter()
        got.append({r[0] for r in cur.execute(SQL, (q,)).fetchall()})
        ms.append((time.perf_counter() - t0) * 1000)
    print(f"ef_search {ef:3} · recall@10 {np.mean([len(g & t) / 10 for g, t in zip(got, truth)]):.3f} · {np.median(ms):.1f}ms")
