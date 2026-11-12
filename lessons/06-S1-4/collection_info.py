from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")
if client.collection_exists("products_struct_test"):
    client.delete_collection("products_struct_test")
client.create_collection(
    collection_name="products_struct_test",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

info = client.get_collection(collection_name="products_struct_test")
print("세그먼트 수:", info.segments_count)
print("인덱싱 기준값:", info.config.optimizer_config.indexing_threshold)
print("색인된 벡터 수:", info.indexed_vectors_count)
