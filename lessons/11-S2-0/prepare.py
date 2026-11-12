import pandas as pd

N_QUERIES = 500
SEED = 7

ex = pd.read_parquet("raw/shopping_queries_dataset_examples.parquet")
ex = ex[(ex["product_locale"] == "us") & (ex["small_version"] == 1) & (ex["split"] == "test")]

qids = ex["query_id"].drop_duplicates().sample(N_QUERIES, random_state=SEED)
qrels = ex[ex["query_id"].isin(qids)][["query_id", "query", "product_id", "esci_label"]]

wanted = qrels["product_id"].unique().tolist()
products = pd.read_parquet(
    "raw/shopping_queries_dataset_products.parquet",
    columns=["product_id", "product_title", "product_bullet_point", "product_brand", "product_color"],
    filters=[("product_locale", "==", "us"), ("product_id", "in", wanted)],
)

qrels.to_csv("qrels.csv", index=False)
products.to_parquet("products.parquet", index=False)
print("검색어:", qrels["query_id"].nunique(), "개")
print("채점 줄:", len(qrels), "줄", qrels["esci_label"].value_counts().to_dict())
print("상품:", len(products), "개")
