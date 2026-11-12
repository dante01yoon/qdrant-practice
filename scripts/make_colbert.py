# 섹션 5 ColBERT(멀티 벡터) 실습용 토큰 벡터를 만든다(fastembed, answerai-colbert-small-v1). 결과 약 420MB.
from pathlib import Path

import numpy as np
import pandas as pd
from fastembed import LateInteractionTextEmbedding

D = Path(__file__).resolve().parent.parent / "data"
products = pd.read_parquet(D / "products.parquet").fillna("")
model = LateInteractionTextEmbedding("answerdotai/answerai-colbert-small-v1")
texts = [" ".join([r.product_title, r.product_brand, r.product_color, r.product_bullet_point[:600]]) for r in products.itertuples()]
mv = list(model.embed(texts, batch_size=32))
np.save(D / "colbert_tokens.npy", np.concatenate(mv).astype(np.float32))
np.save(D / "colbert_lens.npy", np.array([m.shape[0] for m in mv]))
qv = list(model.query_embed(pd.read_csv(D / "queries.csv")["query"].tolist()))
np.save(D / "colbert_q_tokens.npy", np.concatenate(qv).astype(np.float32))
np.save(D / "colbert_q_lens.npy", np.array([m.shape[0] for m in qv]))
print("상품 토큰 벡터", sum(m.shape[0] for m in mv))
