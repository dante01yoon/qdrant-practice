from qdrant_client import QdrantClient
from qdrant_client.models import Distance, HnswConfigDiff, OptimizersConfigDiff, VectorParams

from embed import embed, model

dim = model.get_sentence_embedding_dimension()
print("bge-m3 차원:", dim, "/ 실제 벡터 길이:", len(embed("silicone spatula")))

client = QdrantClient(url="http://localhost:6333")
if client.collection_exists("products_v2"):
    client.delete_collection("products_v2")
client.create_collection(
    collection_name="products_v2",
    vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
)

cfg = client.get_collection("products_v2").config
print("벡터:", cfg.params.vectors.size, cfg.params.vectors.distance)
print("HNSW m:", cfg.hnsw_config.m, "/ ef_construct:", cfg.hnsw_config.ef_construct)
print("인덱싱 기준값:", cfg.optimizer_config.indexing_threshold)

client.update_collection(
    collection_name="products_v2",
    hnsw_config=HnswConfigDiff(m=32),
    optimizers_config=OptimizersConfigDiff(indexing_threshold=1000),
)
cfg = client.get_collection("products_v2").config
print("바꾼 뒤 m:", cfg.hnsw_config.m, "/ 기준값:", cfg.optimizer_config.indexing_threshold)

from qdrant_client.models import VectorParamsDiff

client.update_collection(
    collection_name="products_v2",
    vectors_config={"": VectorParamsDiff(size=768)},
)
