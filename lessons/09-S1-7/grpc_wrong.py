import numpy as np
import pandas as pd
from qdrant_client import QdrantClient

queries = pd.read_csv("queries.csv")
row = queries.index[queries["query"] == "non metal cooking utensils"][0]
query_vec = np.load("query_vecs.npy")[row].tolist()
client = QdrantClient(url="http://localhost:6333", prefer_grpc=True, grpc_port=6399)
client.query_points(collection_name="products", query=query_vec, limit=1)
