import json
import sys
import time

import numpy as np
import pandas as pd

from search import ask_help, search_products

queries = pd.read_csv("queries.csv")
qrels = pd.read_csv("qrels.csv")
GAIN = {"E": 1.0, "S": 0.1, "C": 0.01, "I": 0.0}


def ndcg10(query_id, found):
    rel = {r.product_id: GAIN[r.esci_label] for r in qrels[qrels["query_id"] == query_id].itertuples()}
    dcg = sum(rel.get(p, 0) / np.log2(k + 2) for k, p in enumerate(found))
    ideal = sorted(rel.values(), reverse=True)[:10]
    return dcg / sum(g / np.log2(k + 2) for k, g in enumerate(ideal))


scores, times = [], []
for q in queries.itertuples():
    t = time.perf_counter()
    found = search_products(q.query)
    times.append(time.perf_counter() - t)
    scores.append(ndcg10(q.query_id, [p["product_id"] for p in found]))
shop = {"ndcg10": round(float(np.mean(scores)), 3), "p50_ms": round(np.percentile(times, 50) * 1000), "p95_ms": round(np.percentile(times, 95) * 1000)}
print("상품", shop)

questions = [json.loads(line) for line in open("wixqa_expertwritten_test.jsonl")]
hits, times, tops = [], [], []
for q in questions:
    t = time.perf_counter()
    r = ask_help(q["question"])
    times.append(time.perf_counter() - t)
    gold = set(q["article_ids"])
    hits.append(bool(gold & {a["article_id"] for a in r["found"]}))
    tops.append(r["found"][0]["score"])
help_ = {"recall5": round(float(np.mean(hits)), 3), "p50_ms": round(np.percentile(times, 50) * 1000), "p95_ms": round(np.percentile(times, 95) * 1000)}
print("고객센터", help_)

off = ["What is the capital of France?", "How do I bake sourdough bread?", "Who won the World Cup in 2018?", "What is the boiling point of water?", "How do I change the oil in my car?",
       "프랑스의 수도는 어디인가요?", "김치찌개 끓이는 법 알려 주세요", "오늘 서울 날씨 어때요?"]
off_tops = [ask_help(q)["found"][0]["score"] for q in off]
print("관계없는 질문 점수", off_tops)
print("전문가 질문 중 담당자로 넘어간 비율", round(float(np.mean(np.array(tops) < 0.5)), 3))

json.dump({"shop": shop, "help": help_}, open("report.json", "w"), indent=2)
ok = shop["ndcg10"] >= 0.60 and help_["recall5"] >= 0.70
print("통과" if ok else "기준 미달")
sys.exit(0 if ok else 1)
