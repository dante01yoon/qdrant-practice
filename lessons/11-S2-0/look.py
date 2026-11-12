import pandas as pd

pd.set_option("display.max_colwidth", 60)

ex = pd.read_parquet("raw/shopping_queries_dataset_examples.parquet")
print("채점표 줄 수:", len(ex))
print("칸 이름:", list(ex.columns))

one = ex[ex["query_id"] == 74209]
print(one.iloc[0])
print("이 검색어에 채점된 상품:", len(one), "개", one["esci_label"].value_counts().to_dict())

prod = pd.read_parquet(
    "raw/shopping_queries_dataset_products.parquet",
    columns=["product_id", "product_title", "product_brand", "product_color"],
    filters=[("product_id", "==", "B08693FP1K")],
)
print(prod.T)
