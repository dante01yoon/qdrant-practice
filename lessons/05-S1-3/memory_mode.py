from qdrant_client import QdrantClient

local_client = QdrantClient(":memory:")
print("메모리 모드 컬렉션 목록:", local_client.get_collections())
