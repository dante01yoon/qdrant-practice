# 45. S5-3 ColBERT로 상품 다시 매기기

## 이 수업에서 하는 일

- 상품 3개를 토큰 벡터로
- 만 개 넣기
- 후보 50개를 ColBERT로
- 과제 풀이 · 후보를 몇 개

## 파일

- `bm25.py`
- `colbert_cands.py`
- `colbert_search.py`
- `colbert_try.py`
- `fusion_eval.py`
- `load_colbert.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/45-S5-3
# 앞 수업에서 만든 상태(컬렉션 등)를 먼저 만들어 둡니다. 앞 수업을 이미 따라왔다면 건너뛰어도 됩니다.
uv run python ../../scripts/warmup/hy_helper.py
uv run python load_colbert.py

# 녹화에서 실행한 순서
uv run colbert_try.py
uv run load_colbert.py
uv run colbert_search.py
uv run colbert_cands.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `colbert_lens.npy` → `data/colbert_lens.npy` (저장소에 없음: `scripts/make_colbert.py`로 만듭니다)
- `colbert_q_lens.npy` → `data/colbert_q_lens.npy` (저장소에 없음: `scripts/make_colbert.py`로 만듭니다)
- `colbert_q_tokens.npy` → `data/colbert_q_tokens.npy` (저장소에 없음: `scripts/make_colbert.py`로 만듭니다)
- `colbert_tokens.npy` → `data/colbert_tokens.npy` (저장소에 없음: `scripts/make_colbert.py`로 만듭니다)
- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)
- `qrels.csv` → `data/qrels.csv` (저장소에 들어 있음)
- `queries.csv` → `data/queries.csv` (저장소에 들어 있음)
- `query_vecs.npy` → `data/query_vecs.npy` (저장소에 들어 있음)

