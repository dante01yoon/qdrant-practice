import time

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchText, TextIndexParams, TextIndexType, TokenizerType

client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
N = "products_final"
WORDS = ["silicone", "silicon", "sil", "cooking utensil"]


def has(text):
    return Filter(must=[FieldCondition(key="title", match=MatchText(text=text))])


def check(label):
    times = []
    for _ in range(50):
        t0 = time.perf_counter()
        client.count(N, count_filter=has("silicone"))
        times.append((time.perf_counter() - t0) * 1000)
    counts = {w: client.count(N, count_filter=has(w)).count for w in WORDS}
    print(f"{label:10} {counts} · silicone 세기 {sorted(times)[25]:.2f}ms")


check("인덱스 없음")
for tokenizer in [TokenizerType.WORD, TokenizerType.PREFIX]:
    client.create_payload_index(N, "title", TextIndexParams(type=TextIndexType.TEXT, tokenizer=tokenizer, lowercase=True), wait=True)
    check(tokenizer.value)
    client.delete_payload_index(N, "title", wait=True)
