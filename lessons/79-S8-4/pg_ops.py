import time

import numpy as np
import psycopg
from pgvector.psycopg import register_vector

conn = psycopg.connect("postgresql://postgres:course@localhost:5434/postgres", autocommit=True, prepare_threshold=None)
register_vector(conn)
cur = conn.cursor()


def size():
    return cur.execute("SELECT pg_size_pretty(pg_table_size('shop')), pg_size_pretty(pg_indexes_size('shop'))").fetchone()


print("처음 · 표", *size())
vecs = np.load("product_vecs.npy")
ids = [r[0] for r in cur.execute("SELECT product_id FROM shop ORDER BY product_id").fetchall()]
t = time.perf_counter()
for round_ in range(3):
    cur.executemany("UPDATE shop SET embedding = %s WHERE product_id = %s", [(vecs[(i + round_ + 1) % len(ids)], p) for i, p in enumerate(ids)])
print(f"전체 세 번 고침 {time.perf_counter() - t:.0f}초 · 표", *size())
t = time.perf_counter()
cur.execute("VACUUM shop")
print(f"VACUUM {time.perf_counter() - t:.0f}초 · 표", *size())
t = time.perf_counter()
cur.execute("VACUUM FULL shop")
print(f"VACUUM FULL {time.perf_counter() - t:.0f}초 · 표", *size())
