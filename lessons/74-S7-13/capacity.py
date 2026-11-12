import math

GiB = 1024 ** 3
points, dim, m, replicas = 1215854, 1024, 16, 2
node_ram = 4 * GiB

base = points * replicas
ram = (base * dim * 4 + base * m * 2 * 4 * 1.2 + base * 52) * 1.2
print(f"양자화 없음 · RAM {ram / GiB:.1f}GiB · 노드 {math.ceil(ram / (node_ram * 0.8))}대")

small = (base * dim * 0.5 + base * m * 2 * 4 * 1.2 + base * 52) * 1.2
print(f"bits4 · 원래 벡터는 디스크 · RAM {small / GiB:.1f}GiB · 노드 {max(replicas, math.ceil(small / (node_ram * 0.8)))}대")
