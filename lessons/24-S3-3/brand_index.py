from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType

client = QdrantClient(url="http://localhost:6333")
N = "products_final"

client.create_payload_index(N, "brand", PayloadSchemaType.KEYWORD, wait=True)
info = client.get_collection(N).payload_schema["brand"]
print("brand 인덱스:", info.data_type, "· 들어간 점", info.points, "/ 전체", client.count(N).count)
