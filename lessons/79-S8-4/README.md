# 79. S8-4 운영 — 이미 있는 것과 새로 들이는 것

## 이 수업에서 하는 일

- 고치면 표가 불어난다

## 파일

- `common.py`
- `pg_ops.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

이 수업은 PostgreSQL + pgvector도 씁니다. 루트 README의 「pgvector 컨테이너」 명령으로 먼저 띄워 두세요.

```bash
cd lessons/79-S8-4
# 녹화에서 실행한 순서
uv run pg_ops.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `qrels.csv` → `data/qrels.csv` (저장소에 들어 있음)
- `queries.csv` → `data/queries.csv` (저장소에 들어 있음)
- `query_vecs.npy` → `data/query_vecs.npy` (저장소에 들어 있음)

