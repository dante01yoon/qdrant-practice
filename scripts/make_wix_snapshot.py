# 섹션 9 load.py가 올리는 data/wix_hybrid.snapshot을 만든다.
# 먼저 wix_full(scripts/build_wix_full.py) → S4-12 wix_build.py로 wix_hybrid 컬렉션을 만들어 둔다.
from pathlib import Path

import requests

D = Path(__file__).resolve().parent.parent / "data"
URL, N = "http://localhost:6333", "wix_hybrid"
name = requests.post(f"{URL}/collections/{N}/snapshots", params={"wait": "true"}, timeout=1800).json()["result"]["name"]
with requests.get(f"{URL}/collections/{N}/snapshots/{name}", stream=True, timeout=1800) as r, open(D / "wix_hybrid.snapshot", "wb") as f:
    r.raise_for_status()
    for block in r.iter_content(1 << 20):
        f.write(block)
requests.delete(f"{URL}/collections/{N}/snapshots/{name}", timeout=60)
print("저장:", D / "wix_hybrid.snapshot")
