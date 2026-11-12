# 61. S6-10 과제 — 메모리를 어디까지 줄일 수 있나

## 이 수업에서 하는 일

- 과제 풀이 · 800MB로 넣어 보기

## 파일

- `common.py`
- `low_memory.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/61-S6-10
# 녹화에서 실행한 순서
uv run low_memory.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `esci_us_titles` → `data/esci_us_titles` (저장소에 없음: `scripts/embed_titles_all.py`로 만듭니다)
- `qrels.csv` → `data/qrels.csv` (저장소에 들어 있음)
- `queries.csv` → `data/queries.csv` (저장소에 들어 있음)
- `query_vecs.npy` → `data/query_vecs.npy` (저장소에 들어 있음)

