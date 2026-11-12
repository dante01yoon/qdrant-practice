# ABO(Amazon Berkeley Objects, CC BY 4.0) 사진 검색 실습용: data/abo_photos.parquet의 상품 3,000개 대표 사진(최대 256px)을 받는다.
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent.parent / "data"
OUT = D / "abo" / "small"
OUT.mkdir(parents=True, exist_ok=True)
S3 = "https://amazon-berkeley-objects.s3.amazonaws.com/images/"
meta = D / "abo" / "images.csv.gz"
if not meta.exists():
    urllib.request.urlretrieve(S3 + "metadata/images.csv.gz", meta)
paths = pd.read_csv(meta).set_index("image_id")["path"]
ids = pd.read_parquet(D / "abo_photos.parquet").image_id.unique()


def fetch(image_id):
    f = OUT / f"{image_id}.jpg"
    if not f.exists():
        urllib.request.urlretrieve(S3 + "small/" + paths[image_id], f)


with ThreadPoolExecutor(8) as ex:
    list(ex.map(fetch, ids))
print("사진:", len(list(OUT.glob("*.jpg"))))
