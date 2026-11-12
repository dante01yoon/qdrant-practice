import time

import numpy as np
import pandas as pd
import psycopg
from pgvector.psycopg import register_vector

queries = pd.read_csv("queries.csv")
query_vec = np.load("query_vecs.npy")[queries.index[queries["query"] == "non metal cooking utensils"][0]]
conn = psycopg.connect("postgresql://postgres:course@localhost:5434/postgres", autocommit=True)
register_vector(conn)
cur = conn.cursor()
cur.execute("SET enable_seqscan = off")
SQL = "SELECT id FROM products WHERE brand = 'OXO' ORDER BY embedding <=> %s LIMIT 10"


def run(label):
    t0 = time.perf_counter()
    ids = [r[0] for r in cur.execute(SQL, (query_vec,)).fetchall()]
    print(f"{label:28} {len(ids)}개 · {(time.perf_counter() - t0) * 1000:5.1f}ms · {ids}")


cur.execute("SET hnsw.iterative_scan = off")
for ef in [40, 400, 1000]:
    cur.execute(f"SET hnsw.ef_search = {ef}")
    run(f"끔 · ef_search {ef}")

cur.execute("SET hnsw.ef_search = 40")
for mode in ["relaxed_order", "strict_order"]:
    cur.execute(f"SET hnsw.iterative_scan = {mode}")
    run(f"{mode}")
