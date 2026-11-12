from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchText, PayloadSchemaType, Range, TextIndexParams, TokenizerType

client = QdrantClient(url="http://localhost:6333")
N = "products_final"


def show():
    for field, info in client.get_collection(N).payload_schema.items():
        print(f"  {field:16} {info.data_type.value:8} 점 {info.points}개")


client.create_payload_index(N, field_name="bullet_count", field_schema=PayloadSchemaType.KEYWORD)
show()
five = Filter(must=[FieldCondition(key="bullet_count", range=Range(gte=5))])
print("특징 5개 이상:", client.count(N, count_filter=five).count)

client.delete_payload_index(N, "bullet_count")
client.create_payload_index(N, field_name="bullet_count", field_schema=PayloadSchemaType.INTEGER)
client.create_payload_index(N, field_name="color", field_schema=PayloadSchemaType.KEYWORD)
client.create_payload_index(N, field_name="has_description", field_schema=PayloadSchemaType.BOOL)
client.create_payload_index(N, field_name="title", field_schema=TextIndexParams(type="text", tokenizer=TokenizerType.WORD, lowercase=True))
print("고친 뒤")
show()
spatula = Filter(must=[FieldCondition(key="title", match=MatchText(text="spatula"))])
print("상품명에 spatula:", client.count(N, count_filter=spatula).count)
