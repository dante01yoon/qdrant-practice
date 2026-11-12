# 83. S9-1 무엇을 만들까 — 요구사항과 데이터

## 이 수업에서 하는 일

- 완성 화면 먼저
- 데이터 눈으로 보기

## 파일

- `look.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/83-S9-1
# 녹화에서 실행한 순서
uv run look.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)
- `qrels.csv` → `data/qrels.csv` (저장소에 들어 있음)
- `queries.csv` → `data/queries.csv` (저장소에 들어 있음)
- `wix_kb_corpus.jsonl` → `data/wix_kb_corpus.jsonl` (저장소에 없음: `scripts/prepare_wixqa.py`로 만듭니다)
- `wixqa_expertwritten_test.jsonl` → `data/wixqa_expertwritten_test.jsonl` (저장소에 없음: `scripts/prepare_wixqa.py`로 만듭니다)

