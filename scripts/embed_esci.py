# 상품 1만 개·검색어 500개를 bge-m3로 벡터로 바꾼다. 저장소 data/에 결과가 이미 들어 있어서 보통은 돌릴 필요 없다.
#   uv run python scripts/embed_esci.py          # product_vecs.npy + query_vecs.npy
#   uv run python scripts/embed_esci.py named    # title_vecs.npy + detail_vecs.npy(이름 붙인 벡터 실습용)
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

D = Path(__file__).resolve().parent.parent / "data"
prod = pd.read_parquet(D / "products.parquet").fillna("")
model = SentenceTransformer("BAAI/bge-m3")
model.max_seq_length = 256
t = time.time()

if "named" in sys.argv:
    title = model.encode(prod.product_title.tolist(), batch_size=32, normalize_embeddings=True)
    np.save(D / "title_vecs.npy", title.astype(np.float32))
    has = prod.product_bullet_point != ""
    detail = np.zeros((len(prod), 1024), np.float32)
    detail[has.values] = model.encode(prod.product_bullet_point[has].str[:600].tolist(), batch_size=32, normalize_embeddings=True)
    np.save(D / "detail_vecs.npy", detail)
else:
    def doc_text(r):
        # 상품명 + 브랜드 + 색상 + 특징 앞부분 600자
        parts = [r.product_title, f"Brand: {r.product_brand}" if r.product_brand else "",
                 f"Color: {r.product_color}" if r.product_color else "", (r.product_bullet_point or "")[:600]]
        return "\n".join(p for p in parts if p)

    vecs = model.encode([doc_text(r) for r in prod.itertuples()], batch_size=32, normalize_embeddings=True, show_progress_bar=True)
    np.save(D / "product_vecs.npy", vecs.astype(np.float32))
    q = pd.read_csv(D / "queries.csv")
    np.save(D / "query_vecs.npy", model.encode(q["query"].tolist(), batch_size=64, normalize_embeddings=True).astype(np.float32))
print("끝, 걸린 시간", round(time.time() - t), "초")
