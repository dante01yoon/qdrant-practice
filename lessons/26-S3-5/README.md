# 26. S3-5 필터는 검색 중에 걸린다 — 원리와 10만 개 실측

## 이 수업에서 하는 일

- 10만 개 넣기
- 비율별로 재기
- 과제 풀이 · 0.99를 넘는 ef

## 파일

- `filter_ratio.py`
- `load_100k.py`
- `solution/` — 과제 풀이(같은 파일을 고친 버전이라 따로 둠): `filter_ratio.py`, `find_ef.py`, `load_100k.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/26-S3-5
# 녹화에서 실행한 순서
uv run load_100k.py
uv run filter_ratio.py
```

과제 풀이:

```bash
cd lessons/26-S3-5/solution
# 앞 수업에서 만든 상태(컬렉션 등)를 먼저 만들어 둡니다. 앞 수업을 이미 따라왔다면 건너뛰어도 됩니다.
uv run python load_100k.py

# 녹화에서 실행한 순서
uv run find_ef.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `query_vecs.npy` → `data/query_vecs.npy` (저장소에 들어 있음)
- `us_product_ids.parquet` → `data/esci_us_titles/product_ids.parquet` (저장소에 없음: `scripts/embed_titles_all.py 100000`로 만듭니다)
- `vecs_0000000.npy` → `data/esci_us_titles/vecs_0000000.npy` (저장소에 없음: `scripts/embed_titles_all.py 100000`로 만듭니다)
- `vecs_0050000.npy` → `data/esci_us_titles/vecs_0050000.npy` (저장소에 없음: `scripts/embed_titles_all.py 100000`로 만듭니다)

