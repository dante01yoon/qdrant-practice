# 미국 상품 전체(약 121만 개) 상품명 벡터 — 섹션 3 비율별 필터(10만)·섹션 6 메모리·속도(121만) 실측용.
# 노트북에서 오래 걸려서(약 1시간 이상) 이어서 돌릴 수 있게 5만 개씩 저장한다. 결과는 data/esci_us_titles/ (약 5GB).
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"  # 먼저 scripts/prepare_esci.py --raw-only
OUT = Path(__file__).resolve().parent.parent / "data" / "esci_us_titles"
OUT.mkdir(parents=True, exist_ok=True)
ids_path = OUT / "product_ids.parquet"
if not ids_path.exists():
    p = pd.read_parquet(RAW / "shopping_queries_dataset_products.parquet", columns=["product_id", "product_title", "product_brand", "product_color"],
                        filters=[("product_locale", "==", "us")]).drop_duplicates("product_id").reset_index(drop=True)
    p.to_parquet(ids_path, index=False)
p = pd.read_parquet(ids_path)
limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(p)
model = SentenceTransformer("BAAI/bge-m3"); model.max_seq_length = 64
STEP = 50_000
for start in range(0, limit, STEP):
    f = OUT / f"vecs_{start:07d}.npy"
    if f.exists():
        continue
    titles = p.product_title.fillna("").iloc[start:min(start + STEP, limit)].tolist()
    np.save(f, model.encode(titles, batch_size=64, normalize_embeddings=True).astype(np.float32))
    print(start + len(titles), "/", limit, flush=True)
