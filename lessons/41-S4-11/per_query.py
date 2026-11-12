import numpy as np
import pandas as pd

from fusion_eval import METHODS, N, client, ndcg10, queries, query_vecs

rows = []
for i, q in enumerate(queries.itertuples()):
    row = {"query": q.query}
    for name in ["dense", "sparse", "dbsf"]:
        hits = client.query_points(N, limit=10, with_payload=["product_id"], **METHODS[name](query_vecs[i].tolist(), q.query)).points
        row[name] = ndcg10(q.query_id, [h.payload["product_id"] for h in hits])
    rows.append(row)
df = pd.DataFrame(rows)
df["diff"] = df["sparse"] - df["dense"]


print("단어가 크게 이김:", (df["diff"] > 0.05).sum(), "/ 벡터가 크게 이김:", (df["diff"] < -0.05).sum(), "/ 비슷:", (df["diff"].abs() <= 0.05).sum())
print("\n[단어가 이긴 검색어]")
print(df.sort_values("diff", ascending=False).head(5)[["query", "dense", "sparse", "dbsf"]].round(2).to_string(index=False))
print("\n[벡터가 이긴 검색어]")
print(df.sort_values("diff").head(5)[["query", "dense", "sparse", "dbsf"]].round(2).to_string(index=False))
has_digit = df["query"].str.contains(r"\d")
print("\n숫자가 든 검색어", has_digit.sum(), "개 · dense", round(df[has_digit]["dense"].mean(), 3), "· sparse", round(df[has_digit]["sparse"].mean(), 3), "· dbsf", round(df[has_digit]["dbsf"].mean(), 3))
