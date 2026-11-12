# 27. S3-7 아주 좁은 필터

## 이 수업에서 하는 일

- 브랜드로 좁히기
- 점수 기준과 빈 결과
- 과제 풀이 · 모자라면 채우기

## 파일

- `fallback.py`
- `narrow.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/27-S3-7
# 앞 수업에서 만든 상태(컬렉션 등)를 먼저 만들어 둡니다. 앞 수업을 이미 따라왔다면 건너뛰어도 됩니다.
uv run python ../../scripts/warmup/warm_final.py

# 녹화에서 실행한 순서
uv run narrow.py
uv run fallback.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `detail_vecs.npy` → `data/detail_vecs.npy` (저장소에 들어 있음)
- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)
- `queries.csv` → `data/queries.csv` (저장소에 들어 있음)
- `query_vecs.npy` → `data/query_vecs.npy` (저장소에 들어 있음)
- `title_vecs.npy` → `data/title_vecs.npy` (저장소에 들어 있음)

