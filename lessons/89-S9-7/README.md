# 89. S9-7 배포 — 컨테이너로 묶어서 띄우기

## 이 수업에서 하는 일

- 컨테이너로 띄우기

## 파일

- `Dockerfile`
- `app.py`
- `compose.yaml`
- `index.html`
- `load.py`
- `search.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/89-S9-7
# 녹화에서 실행한 순서
docker compose -p qdshop up -d
QDRANT_URL=http://localhost:6340 QDRANT_GRPC=6341 uv run load.py
until curl -sf localhost:8090/health; do sleep 2; done
curl -s 'localhost:8090/search?q=wireless+mouse' | python3 -m json.tool | head -8
docker exec qdshop-app-1 python -c 'import os; os.kill(1, 15)'
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)
- `shop_vocab.json` → `data/shop_vocab.json` (저장소에 들어 있음)
- `wix_hybrid.snapshot` → `data/wix_hybrid.snapshot` (저장소에 없음: `scripts/make_wix_snapshot.py (먼저 S4-12 wix_build.py)`로 만듭니다)
- `wix_vocab.json` → `data/wix_vocab.json` (저장소에 들어 있음)

