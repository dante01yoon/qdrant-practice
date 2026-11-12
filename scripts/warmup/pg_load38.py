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
