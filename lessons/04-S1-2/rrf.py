def rrf_score(rank1, rank2, k, start=1):
    r1, r2 = rank1 - 1 + start, rank2 - 1 + start
    return 1.0 / (k + r1) + 1.0 / (k + r2)


print("논문 방식 k=60:", round(rrf_score(1, 3, k=60), 4))
print("논문 방식 k=2:", round(rrf_score(1, 3, k=2), 4))
print("Qdrant 방식 k=2:", round(rrf_score(1, 3, k=2, start=0), 4))
