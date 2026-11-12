import glob
import subprocess
import time

import numpy as np
import requests
from qdrant_client import QdrantClient, models

D = "esci_us_titles"  # scripts/embed_titles_all.py가 만드는 폴더(data/esci_us_titles)
files = sorted(glob.glob(f"{D}/vecs_*.npy"))
parts = [np.load(f, mmap_mode="r") for f in files]
total = sum(len(p) for p in parts)
queries = np.load("query_vecs.npy")[:100]
U = "http://localhost:6412"
MB = 1024 * 1024
print("벡터", total, "파일", len(files), flush=True)


def batches():
    i = 0
    for p in parts:
        for s in range(0, len(p), 500):
            yield range(i + s, i + s + min(500, len(p) - s)), p[s:s + 500]
        i += len(p)


def up():
    subprocess.run(["docker", "rm", "-f", "qd-big"], capture_output=True)
    subprocess.run(["docker", "volume", "rm", "-f", "qd_big"], capture_output=True)
    subprocess.run(["docker", "run", "-d", "--name", "qd-big", "-p", "6412:6333", "-v", "qd_big:/qdrant/storage", "--memory", "3g", "qdrant/qdrant:v1.20.0"], capture_output=True)
    for _ in range(60):
        try:
            if requests.get(f"{U}/readyz", timeout=1).status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(1)


def stats():
    return subprocess.run(["docker", "stats", "--no-stream", "--format", "{{.MemUsage}}", "qd-big"], capture_output=True, text=True).stdout.strip()


up()
c = QdrantClient(url=U, timeout=600)
M = models.Memory
N = "products_all"
c.create_collection(N, vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE, memory=M.COLD),
                    quantization_config=models.TurboQuantization(turbo=models.TurboQuantQuantizationConfig(bits=models.TurboQuantBitSize.BITS4, memory=M.PINNED)))
t0 = time.time()
for k, (ids, vecs) in enumerate(batches()):
    c.upsert(N, points=models.Batch(ids=list(ids), vectors=vecs.tolist()), wait=k % 200 == 0)
    if k % 500 == 0:
        print(f"넣는 중 {ids[0]} · {time.time() - t0:.0f}초 · {stats()}", flush=True)
print(f"넣기 끝 {time.time() - t0:.0f}초", flush=True)
while (i := c.get_collection(N)).status != models.CollectionStatus.GREEN or i.indexed_vectors_count < 0.9 * total:
    print(f"색인 중 {i.indexed_vectors_count} · {time.time() - t0:.0f}초 · {stats()}", flush=True)
    time.sleep(60)
print(f"색인 끝 {time.time() - t0:.0f}초 · {stats()}", flush=True)
time.sleep(10)
v = requests.get(f"{U}/collections/{N}/memory").json()["result"]["vectors"][0]
print({k: {"disk": round(x["disk_bytes"] / MB), "ram": round(x["ram_bytes"] / MB), "cache": round(x["expected_cache_bytes"] / MB)} for k, x in v.items() if isinstance(x, dict)}, flush=True)
print("du", subprocess.run(["docker", "exec", "qd-big", "du", "-sh", f"/qdrant/storage/collections/{N}"], capture_output=True, text=True).stdout.strip(), flush=True)


def run(params, n=100):
    got, ms = [], []
    for q in queries[:n]:
        t = time.perf_counter()
        got.append({p.id for p in c.query_points(N, query=q.tolist(), limit=10, search_params=params).points})
        ms.append((time.perf_counter() - t) * 1000)
    return got, np.median(ms), np.percentile(ms, 95)


truth, a, b = run(models.SearchParams(exact=True), 20)
print(f"exact 20개 · 가운데 {a:.0f}ms", flush=True)
Q = models.QuantizationSearchParams
for label, p in [("rescore 끔", Q(rescore=False)), ("rescore 켬", Q(rescore=True)), ("rescore 켬 oversampling 4", Q(rescore=True, oversampling=4.0))]:
    got, med, p95 = run(models.SearchParams(quantization=p))
    rc = np.mean([len(g & t) / 10 for g, t in zip(got[:20], truth)])
    print(f"{label} · recall@10(20개) {rc:.3f} · 가운데 {med:.1f}ms · 95% {p95:.1f}ms · {stats()}", flush=True)
subprocess.run(["docker", "rm", "-f", "qd-big"], capture_output=True)
subprocess.run(["docker", "volume", "rm", "-f", "qd_big"], capture_output=True)
print("ALLDONE", flush=True)
