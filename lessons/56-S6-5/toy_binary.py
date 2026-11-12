import numpy as np

vecs = np.load("vecs_100k.npy", mmap_mode="r")[:20000].copy()
queries = np.load("query_vecs.npy")[:200]
codes = vecs > 0
print("숫자", vecs[0][:4].round(3), "→ 비트", codes[0][:4].astype(int))

overlap = {10: [], 40: [], 100: []}
for q in queries:
    top_cos = set(np.argsort(-(vecs @ q))[:10])
    diff = (codes != (q > 0)).sum(axis=1)
    rank = np.argsort(diff)
    for k in overlap:
        overlap[k].append(len(top_cos & set(rank[:k])) / 10)
for k, v in overlap.items():
    print(f"다른 칸이 적은 {k:3}개 안에 진짜 가까운 10개 중 {np.mean(v) * 10:.1f}개")
