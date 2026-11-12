import glob
import subprocess
import sys
import time

import numpy as np
from qdrant_client import QdrantClient, models

LIMIT = sys.argv[1] if len(sys.argv) > 1 else "800m"
D = "esci_us_titles"  # scripts/embed_titles_all.py가 만드는 폴더(data/esci_us_titles)
parts = [np.load(f, mmap_mode="r") for f in sorted(glob.glob(f"{D}/vecs_*.npy"))]
total = sum(len(p) for p in parts)


def docker(*args):
    return subprocess.run(["docker", *args], capture_output=True, text=True).stdout.strip()


docker("rm", "-f", "qd-low")
docker("volume", "rm", "-f", "qd_low")
docker("run", "-d", "--name", "qd-low", "-p", "6413:6333", "-v", "qd_low:/qdrant/storage", "--memory", LIMIT, "qdrant/qdrant:v1.20.0")
time.sleep(5)
print("메모리 한도", LIMIT, "· 넣을 벡터", total)

client = QdrantClient(url="http://localhost:6413", timeout=60)
M = models.Memory
client.create_collection("all", vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE, memory=M.COLD),
                         quantization_config=models.TurboQuantization(turbo=models.TurboQuantQuantizationConfig(bits=models.TurboQuantBitSize.BITS4, memory=M.PINNED)))

done, t0 = 0, time.time()
try:
    for part in parts:
        for s in range(0, len(part), 500):
            batch = part[s:s + 500]
            client.upsert("all", points=models.Batch(ids=list(range(done, done + len(batch))), vectors=batch.tolist()), wait=False)
            done += len(batch)
            if done % 100000 == 0:
                print(f"{done:>9}개 · {time.time() - t0:.0f}초 · {docker('stats', '--no-stream', '--format', '{{.MemUsage}}', 'qd-low')}", flush=True)
    print("다 넣음", done)
except Exception as e:
    print(f"{done}개에서 멈춤 · {type(e).__name__}")
time.sleep(3)
print("메모리 부족으로 죽었나:", docker("inspect", "qd-low", "--format", "{{.State.OOMKilled}}"))
docker("rm", "-f", "qd-low")
docker("volume", "rm", "-f", "qd_low")
