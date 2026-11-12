# 32. S4-2 BM25를 sparse로

## 이 수업에서 하는 일

- 토큰과 사전
- BM25 값
- 넣고 찾기
- 500개로 재기
- 과제 풀이 · k1과 b 바꿔 보기
- Qdrant 안의 BM25

## 파일

- `bm25.py`
- `builtin_bm25.py`
- `score_bm25.py`
- `tune_kb.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/32-S4-2
# 녹화에서 실행한 순서
uv run bm25.py
uv run score_bm25.py
uv run tune_kb.py
uv run builtin_bm25.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)
- `qrels.csv` → `data/qrels.csv` (저장소에 들어 있음)
- `queries.csv` → `data/queries.csv` (저장소에 들어 있음)

