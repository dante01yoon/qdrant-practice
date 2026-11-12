# 16. S2-5 upsert와 다시 돌려도 안전한 적재

## 이 수업에서 하는 일

- 다시 돌려도 되는 적재
- 끊기고, 다시, 또 다시
- upsert는 통째로 바꾼다
- 과제 풀이 · 끊고, 다시, 확인
- 망가진 메모는?

## 파일

- `check.py`
- `load.py`
- `overwrite.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/16-S2-5
# 앞 수업에서 만든 상태(컬렉션 등)를 먼저 만들어 둡니다. 앞 수업을 이미 따라왔다면 건너뛰어도 됩니다.
uv run python load.py
uv run python ../../scripts/warmup/warm_overwrite.py

# 녹화에서 실행한 순서
uv run load.py 7
uv run load.py
uv run overwrite.py
uv run load.py 15
uv run check.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)

