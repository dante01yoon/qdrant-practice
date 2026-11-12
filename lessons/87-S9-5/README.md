# 87. S9-5 화면 — 손님이 쓰는 모습으로

## 이 수업에서 하는 일

- 화면 파일 만들기
- 직접 써 보기

## 파일

- `app.py`
- `index.html`
- `search.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/87-S9-5
# 녹화에서 실행한 순서
uv run uvicorn app:app --port 8000 --log-level warning > server.log 2>&1 &
until curl -sf localhost:8000/health > /dev/null; do sleep 1; done
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `shop_vocab.json` → `data/shop_vocab.json` (저장소에 들어 있음)
- `wix_vocab.json` → `data/wix_vocab.json` (저장소에 들어 있음)

