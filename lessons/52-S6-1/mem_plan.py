GiB = 1024 ** 3
n, dim, m = 1215854, 1024, 16

vectors = n * dim * 4
hnsw = n * m * 2 * 4 * 1.2
ids = n * 52
print(f"벡터 {vectors / GiB:.2f}GiB · HNSW {hnsw / GiB:.2f}GiB · ID {ids / GiB:.2f}GiB")

total = (vectors + hnsw + ids) * 1.2
print(f"여유 20%까지 {total / GiB:.2f}GiB")
print(f"복제 2개면 {total * 2 / GiB:.2f}GiB")
