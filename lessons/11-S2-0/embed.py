import time

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

products = pd.read_parquet("products.parquet").fillna("")


def doc_text(row):
    parts = [
        row.product_title,
        f"Brand: {row.product_brand}" if row.product_brand else "",
        f"Color: {row.product_color}" if row.product_color else "",
        row.product_bullet_point[:600],
    ]
    return "\n".join(p for p in parts if p)


texts = [doc_text(row) for row in products.itertuples()]
print(texts[0])

model = SentenceTransformer("BAAI/bge-m3")
model.max_seq_length = 256

t0 = time.perf_counter()
vecs = model.encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=True)
print("걸린 시간:", round(time.perf_counter() - t0), "초, 모양:", vecs.shape)
np.save("product_vecs.npy", vecs.astype(np.float32))
