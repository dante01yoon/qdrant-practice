# 섹션 6·8 실습용 vecs_100k.npy: 미국 상품명 벡터 앞 10만 개(먼저 scripts/embed_titles_all.py 100000)
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent.parent / "data"
parts = [np.load(D / "esci_us_titles" / f"vecs_{s:07d}.npy") for s in (0, 50_000)]
np.save(D / "vecs_100k.npy", np.concatenate(parts))
print("vecs_100k.npy", sum(len(p) for p in parts))
