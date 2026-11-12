# 아마존 ESCI 원본(Apache-2.0, github.com/amazon-science/esci-data)을 받아 실습용 부분 집합을 만든다.
# 저장소의 data/에 이미 들어 있는 products.parquet·qrels.csv·queries.csv와 같은 파일이 나온다(seed 7).
#   uv run python scripts/prepare_esci.py             # 원본 받기(약 1.2GB) + 부분 집합 만들기
#   uv run python scripts/prepare_esci.py --raw-only  # 원본만 받기(S2-0 실습, 미국 상품 121만 개 벡터용)
import sys
import urllib.request
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent.parent / "data"
RAW = D / "raw"
URL = "https://github.com/amazon-science/esci-data/raw/main/shopping_queries_dataset/"
FILES = ["shopping_queries_dataset_examples.parquet", "shopping_queries_dataset_products.parquet"]

RAW.mkdir(parents=True, exist_ok=True)
for f in FILES:
    if not (RAW / f).exists():
        print("받는 중:", f, flush=True)
        urllib.request.urlretrieve(URL + f, RAW / f)
if "--raw-only" in sys.argv:
    sys.exit()

N_QUERIES, SEED = 500, 7
ex = pd.read_parquet(RAW / FILES[0])
ex = ex[(ex.product_locale == "us") & (ex.small_version == 1) & (ex.split == "test")]
qids = ex.query_id.drop_duplicates().sample(N_QUERIES, random_state=SEED)
qrels = ex[ex.query_id.isin(qids)][["query_id", "query", "product_id", "esci_label"]]

cols = ["product_id", "product_title", "product_description", "product_bullet_point", "product_brand", "product_color", "product_locale"]
prod = pd.read_parquet(RAW / FILES[1], columns=cols, filters=[("product_locale", "=", "us")])
prod = prod[prod.product_id.isin(qrels.product_id)].drop(columns="product_locale").drop_duplicates("product_id")

qrels.to_csv(D / "qrels.csv", index=False)
prod.to_parquet(D / "products.parquet", index=False)
qrels.drop_duplicates("query_id")[["query_id", "query"]].reset_index(drop=True).to_csv(D / "queries.csv", index=False)
print("검색어:", qrels.query_id.nunique(), "· 채점 줄:", len(qrels), "· 상품:", len(prod))
