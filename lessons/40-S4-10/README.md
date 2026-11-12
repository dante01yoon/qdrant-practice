# 40. S4-10 평가셋 넓히기 — 고른 방법 다시 확인

## 이 수업에서 하는 일

- 고객센터 질문 200개로 다시
- 과제 풀이 · 고르는 셋과 확인하는 셋

## 파일

- `embed.py`
- `holdout.py`
- `wix_eval.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/40-S4-10
# 녹화에서 실행한 순서
uv run wix_eval.py
uv run holdout.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `wix_vocab.json` → `data/wix_vocab.json` (저장소에 들어 있음)
- `wixqa_expertwritten_test.jsonl` → `data/wixqa_expertwritten_test.jsonl` (저장소에 없음: `scripts/prepare_wixqa.py`로 만듭니다)

