# 마켓(나라)별 상품: 스페인(es)·일본(jp) 평가용 검색어 50개씩의 채점 상품을 떼어 벡터까지 만든다(섹션 3 권한 필터·섹션 7 멀티테넌시)
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"  # 먼저 scripts/prepare_esci.py --raw-only
OUT = Path(__file__).resolve().parent.parent / "data"
ex = pd.read_parquet(RAW / "shopping_queries_dataset_examples.parquet")
ex = ex[ex.product_locale.isin(["es", "jp"]) & (ex.small_version == 1) & (ex.split == "test")]
parts = []
for loc in ["es", "jp"]:
    qids = ex[ex.product_locale == loc].query_id.drop_duplicates().sample(50, random_state=7)
    parts.append(ex[ex.query_id.isin(qids)][["query_id", "query", "product_id", "esci_label", "product_locale"]])
qrels = pd.concat(parts)
prod = pd.read_parquet(RAW / "shopping_queries_dataset_products.parquet",
                       columns=["product_id", "product_title", "product_bullet_point", "product_brand", "product_color", "product_locale"],
                       filters=[("product_locale", "in", ["es", "jp"]), ("product_id", "in", qrels.product_id.unique().tolist())])
prod = prod.merge(qrels[["product_id", "product_locale"]].drop_duplicates(), on=["product_id", "product_locale"]).drop_duplicates(["product_id", "product_locale"]).fillna("")
texts = [f"{r.product_title}\nBrand: {r.product_brand}\n{r.product_bullet_point[:600]}" for r in prod.itertuples()]
model = SentenceTransformer("BAAI/bge-m3"); model.max_seq_length = 256
vecs = model.encode(texts, batch_size=32, normalize_embeddings=True)
prod.to_parquet(OUT / "market_products.parquet", index=False)
qrels.to_csv(OUT / "market_qrels.csv", index=False)
np.save(OUT / "market_vecs.npy", vecs.astype(np.float32))
print(prod.product_locale.value_counts().to_dict(), vecs.shape)
