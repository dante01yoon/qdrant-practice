import time

from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType, TextIndexParams, TokenizerType

client = QdrantClient(url="http://localhost:6333")
N = "products_final"
INDEXES = {
    "color": PayloadSchemaType.KEYWORD,
    "bullet_count": PayloadSchemaType.INTEGER,
    "has_description": PayloadSchemaType.BOOL,
    "title": TextIndexParams(type="text", tokenizer=TokenizerType.WORD, lowercase=True),
}

for field, schema in INDEXES.items():
    t0 = time.perf_counter()
    client.create_payload_index(N, field_name=field, field_schema=schema, wait=True)
    print(f"{field:16} 인덱스 만들기 {(time.perf_counter() - t0) * 1000:6.1f}ms")
print("인덱스:", sorted(client.get_collection(N).payload_schema))
