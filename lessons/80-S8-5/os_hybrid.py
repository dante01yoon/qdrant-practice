import json
import subprocess
import time

import numpy as np
import pandas as pd
import requests

from common import ndcg10, queries, query_vecs, rrf

U = "http://localhost:9201"
subprocess.run(["docker", "rm", "-f", "qd-os"], capture_output=True)
subprocess.run(["docker", "run", "-d", "--name", "qd-os", "-p", "127.0.0.1:9201:9200", "--memory", "3g", "-e", "discovery.type=single-node", "-e", "DISABLE_SECURITY_PLUGIN=true",
                "-e", "DISABLE_INSTALL_DEMO_CONFIG=true", "opensearchproject/opensearch:2.19.0"], capture_output=True)
t = time.perf_counter()
while True:
    try:
        version = requests.get(U, timeout=2).json()["version"]["number"]
        break
    except requests.RequestException:
        time.sleep(2)
print(f"OpenSearch {version} · 켜는 데 {time.perf_counter() - t:.0f}초")

products = pd.read_parquet("products.parquet").fillna("")
vecs = np.load("product_vecs.npy")
requests.put(f"{U}/shop", json={"settings": {"index": {"knn": True, "number_of_shards": 1, "number_of_replicas": 0}},
                                "mappings": {"properties": {"v": {"type": "knn_vector", "dimension": 1024, "space_type": "cosinesimil",
                                                                  "method": {"name": "hnsw", "engine": "faiss", "parameters": {"m": 16, "ef_construction": 100}}},
                                                            "doc": {"type": "text"}, "product_id": {"type": "keyword"}}}}).raise_for_status()

t = time.perf_counter()
for s in range(0, len(products), 500):
    lines = []
    for i in range(s, min(s + 500, len(products))):
        r = products.iloc[i]
        lines.append(json.dumps({"index": {"_index": "shop", "_id": i}}))
        lines.append(json.dumps({"v": vecs[i].tolist(), "product_id": r.product_id, "doc": " ".join([r.product_title, r.product_brand, r.product_color, r.product_bullet_point[:600]])}))
    requests.post(f"{U}/_bulk", data="\n".join(lines) + "\n", headers={"Content-Type": "application/x-ndjson"}, timeout=300).raise_for_status()
requests.post(f"{U}/shop/_refresh", timeout=300)
print(f"넣기 {time.perf_counter() - t:.0f}초")


def ids(body):
    return [h["_source"]["product_id"] for h in requests.post(f"{U}/shop/_search", json={"size": 50, "_source": ["product_id"], **body}).json()["hits"]["hits"]]


res = {"dense": [], "bm25": [], "rrf": []}
for i, q in enumerate(queries.itertuples()):
    d = ids({"query": {"knn": {"v": {"vector": query_vecs[i].tolist(), "k": 50}}}})
    b = ids({"query": {"match": {"doc": q.query}}})
    res["dense"].append(ndcg10(q.query_id, d[:10]))
    res["bm25"].append(ndcg10(q.query_id, b[:10]))
    res["rrf"].append(ndcg10(q.query_id, rrf([d, b])))
for name, values in res.items():
    print(f"{name:6} nDCG@10 {np.mean(values):.3f}")
subprocess.run(["docker", "rm", "-f", "qd-os"], capture_output=True)
