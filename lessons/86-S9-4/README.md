# 86. S9-4 검색 API — 다른 프로그램이 부를 수 있게

## 이 수업에서 하는 일

- 찾는 함수와 API

## 파일

- `app.py`
- `search.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/86-S9-4
# 녹화에서 실행한 순서
uv run uvicorn app:app --port 8000 --log-level warning > server.log 2>&1 &
until curl -sf localhost:8000/health > /dev/null; do sleep 1; done
curl -s localhost:8000/health
curl -s localhost:8000/search | python3 -m json.tool | head -12
curl -s 'localhost:8000/search?q=wireless+mouse&color=Black' | python3 -m json.tool | head -14
curl -s 'localhost:8000/ask?q=How+do+I+connect+my+domain' | python3 -m json.tool | cut -c1-90 | head -6
curl -s -G localhost:8000/ask --data-urlencode 'q=김치찌개 끓이는 법' | python3 -m json.tool | cut -c1-90 | head -6
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `shop_vocab.json` → `data/shop_vocab.json` (저장소에 들어 있음)
- `wix_vocab.json` → `data/wix_vocab.json` (저장소에 들어 있음)

