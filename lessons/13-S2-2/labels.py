import numpy as np
import pandas as pd
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
queries = pd.read_csv("queries.csv")
row = queries.index[queries["query"] == "non metal cooking utensils"][0]
query_vec = np.load("query_vecs.npy")[row].tolist()

qrels = pd.read_csv("qrels.csv")
labels = qrels[qrels["query_id"] == 74209].set_index("product_id")["esci_label"]

hits = client.query_points("products_uuid", query=query_vec, limit=10).points
for rank, p in enumerate(hits, start=1):
    pid = p.payload["product_id"]
    print(rank, labels.get(pid, "-"), pid, p.payload["title"][:35])
