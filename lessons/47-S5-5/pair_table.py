import numpy as np
import pandas as pd
from PIL import Image
from sentence_transformers import SentenceTransformer

items = pd.read_parquet("abo_photos.parquet")
model = SentenceTransformer("clip-ViT-B-32")

picked = pd.concat([items[items.type == t].head(1) for t in ["CHAIR", "SHOES", "COFFEE", "RUG", "LAMP"]])
photos = model.encode([Image.open(f"small/{i}.jpg").convert("RGB") for i in picked.image_id], normalize_embeddings=True)
names = model.encode(picked.name.str[:60].tolist(), normalize_embeddings=True)

table = photos @ names.T
print("        " + "  ".join(f"{t[:6]:>6}" for t in picked.type))
for t, row in zip(picked.type, table):
    print(f"{t[:6]:>6}  " + "  ".join(f"{v:6.3f}" for v in row))
print("줄마다 가장 큰 칸이 자기 짝인가:", [int(np.argmax(row)) == k for k, row in enumerate(table)])
