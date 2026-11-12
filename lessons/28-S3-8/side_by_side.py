import numpy as np
import pandas as pd
import psycopg
from pgvector.psycopg import register_vector

products = pd.read_parquet("products.parquet")
vecs = np.load("product_vecs.npy")
queries = pd.read_csv("queries.csv")
query_vec = np.load("query_vecs.npy")[queries.index[queries["query"] == "non metal cooking utensils"][0]]

conn = psycopg.connect("postgresql://postgres:course@localhost:5434/postgres", autocommit=True)
register_vector(conn)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS products")
cur.execute("CREATE TABLE products (id int PRIMARY KEY, title text, brand text, embedding vector(1024))")
with cur.copy("COPY products (id, title, brand, embedding) FROM STDIN WITH (FORMAT BINARY)") as copy:
    copy.set_types(["int4", "text", "text", "vector"])
    for i, r in enumerate(products.itertuples()):
        copy.write_row([i, r.product_title, r.product_brand if isinstance(r.product_brand, str) else None, vecs[i]])
cur.execute("CREATE INDEX ON products USING hnsw (embedding vector_cosine_ops)")
print("넣은 줄:", cur.execute("SELECT count(*) FROM products").fetchone()[0])

SQL = "SELECT title FROM products WHERE brand = %s ORDER BY embedding <=> %s LIMIT 10"
cur.execute("SET enable_seqscan = off")

for mode in ["off", "relaxed_order"]:
    cur.execute(f"SET hnsw.iterative_scan = {mode}")
    for brand in ["OXO", "Nike", "Amazon Basics"]:
        rows = cur.execute(SQL, (brand, query_vec)).fetchall()
        print(f"iterative_scan={mode:13} | {brand:13} | {len(rows)}개")

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

qc = QdrantClient(url="http://localhost:6333")
for brand in ["OXO", "Nike", "Amazon Basics"]:
    f = Filter(must=[FieldCondition(key="brand", match=MatchValue(value=brand))])
    hits = qc.query_points("products_final", query=query_vec.tolist(), using="all", query_filter=f, limit=10).points
    print(f"Qdrant                       | {brand:13} | {len(hits)}개")
