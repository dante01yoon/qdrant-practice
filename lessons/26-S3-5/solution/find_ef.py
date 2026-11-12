from filter_ratio import keep, measure

for ef in [128, 256, 384, 512]:
    recall, ms = measure(keep(500), ef)
    print(f"hnsw_ef={ef:3} recall {recall:.3f} · {ms:.2f}ms" + ("  ← 0.99 넘음" if recall >= 0.99 else ""))
    if recall >= 0.99:
        break
