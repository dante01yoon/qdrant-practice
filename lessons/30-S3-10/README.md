# 30. S3-10 과제·풀이

## 이 수업에서 하는 일

- 조건을 골라 받는 필터
- 검색 함수와 실행
- 색상을 낱말로

## 파일

- `embed.py`
- `search.py`
- `search_v2.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/30-S3-10
# 앞 수업에서 만든 상태(컬렉션 등)를 먼저 만들어 둡니다. 앞 수업을 이미 따라왔다면 건너뛰어도 됩니다.
uv run python ../../scripts/warmup/warm_final.py
uv run python ../../scripts/warmup/warm_idx.py

# 녹화에서 실행한 순서
uv run search.py
uv run search_v2.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `detail_vecs.npy` → `data/detail_vecs.npy` (저장소에 들어 있음)
- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)
- `title_vecs.npy` → `data/title_vecs.npy` (저장소에 들어 있음)

