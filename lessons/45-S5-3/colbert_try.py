import pandas as pd
from fastembed import LateInteractionTextEmbedding

products = pd.read_parquet("products.parquet").fillna("")
model = LateInteractionTextEmbedding("answerdotai/answerai-colbert-small-v1")

texts = [" ".join([r.product_title, r.product_brand, r.product_color, r.product_bullet_point[:600]])
         for r in products.head(3).itertuples()]
for text, tokens in zip(texts, model.embed(texts)):
    print(tokens.shape, text[:40])
