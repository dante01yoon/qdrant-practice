# 88. S9-6 평가와 성적표 — 끝났다고 말할 근거

## 이 수업에서 하는 일

- 성적표 만들기

## 파일

- `eval.py`
- `search.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/88-S9-6
# 녹화에서 실행한 순서
uv run eval.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `qrels.csv` → `data/qrels.csv` (저장소에 들어 있음)
- `queries.csv` → `data/queries.csv` (저장소에 들어 있음)
- `shop_vocab.json` → `data/shop_vocab.json` (저장소에 들어 있음)
- `wix_vocab.json` → `data/wix_vocab.json` (저장소에 들어 있음)
- `wixqa_expertwritten_test.jsonl` → `data/wixqa_expertwritten_test.jsonl` (저장소에 없음: `scripts/prepare_wixqa.py`로 만듭니다)

