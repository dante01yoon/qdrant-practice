import time

import numpy as np
import requests
from qdrant_client import models

from quant_helper import N, client, no_rescore, queries, recall, run, vecs, with_rescore

MB = 1024 * 1024
M = models.Memory


def build(dense, small):
    if client.collection_exists(N):
        client.delete_collection(N)
    client.create_collection(N, vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE, memory=dense),
                             quantization_config=models.TurboQuantization(turbo=models.TurboQuantQuantizationConfig(bits=models.TurboQuantBitSize.BITS4, memory=small)))
    client.upload_collection(N, vectors=vecs, ids=range(len(vecs)), batch_size=500, wait=True)
    while (info := client.get_collection(N)).status != models.CollectionStatus.GREEN or info.indexed_vectors_count < 0.9 * len(vecs):
        time.sleep(0.5)
    time.sleep(5)


truth = None
for name, dense, small in [("기본", None, None), ("원래 cold", M.COLD, None), ("원래 cold + 작은 pinned", M.COLD, M.PINNED)]:
    build(dense, small)
    truth = truth or run(models.SearchParams(exact=True))[0]
    v = requests.get(f"http://localhost:6333/collections/{N}/memory").json()["result"]["vectors"][0]
    print(f"{name} · 원래 있어야 할 캐시 {v['storage']['expected_cache_bytes'] / MB:.0f}MB · 작은 벡터 RAM {v['quantized']['ram_bytes'] / MB:.0f}MB · 있어야 할 캐시 {v['quantized']['expected_cache_bytes'] / MB:.0f}MB", flush=True)
    for label, params in [("rescore 끔", no_rescore()), ("rescore 켬", with_rescore())]:
        got, ms = run(params)
        print(f"  {label} · recall@10 {recall(got, truth):.3f} · {ms:.1f}ms", flush=True)
