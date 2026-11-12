import time

import requests
from qdrant_client import models

from quant_helper import N, build, client

build(None)
MB = 1024 * 1024


def show(title):
    v = requests.get(f"http://localhost:6333/collections/{N}/memory").json()["result"]["vectors"][0]
    small = v.get("quantized", {"ram_bytes": 0})["ram_bytes"]
    print(f"{title} · 원래 벡터 있어야 할 캐시 {v['storage']['expected_cache_bytes'] / MB:.0f}MB · 작은 벡터 RAM {small / MB:.0f}MB")


show("켜기 전")
client.update_collection(N, quantization_config=models.ScalarQuantization(scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8)))
time.sleep(1)
t0 = time.perf_counter()
while client.get_collection(N).status != models.CollectionStatus.GREEN:
    time.sleep(0.5)
print(f"양자화 벡터 만드는 데 {time.perf_counter() - t0:.0f}초")
show("켠 뒤")
