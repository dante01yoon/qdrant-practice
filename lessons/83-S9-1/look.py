import json

import pandas as pd

products = pd.read_parquet("products.parquet")
queries = pd.read_csv("queries.csv")
qrels = pd.read_csv("qrels.csv")
print("상품", len(products), "· 검색어", len(queries), "· 정답표", len(qrels))
print(products.iloc[0][["product_title", "product_brand", "product_color"]].to_dict())
print(queries["query"].iloc[0])

articles = [json.loads(line) for line in open("wix_kb_corpus.jsonl")]
questions = [json.loads(line) for line in open("wixqa_expertwritten_test.jsonl")]
print("고객센터 글", len(articles), "· 전문가 질문", len(questions))
print(articles[0]["title"], "·", articles[0]["url"])
print(questions[0]["question"])
print("정답 글", questions[0]["article_ids"][0][:12])
