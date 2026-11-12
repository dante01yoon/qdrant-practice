# 14. S2-3 payload 설계

## 이 수업에서 하는 일

- payload 만드는 함수
- 넣고 세기
- 숫자는 숫자로
- 과제 풀이 · 참 거짓 칸

## 파일

- `payload.py`
- `solution/` — 과제 풀이(같은 파일을 고친 버전이라 따로 둠): `payload.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/14-S2-3
# 녹화에서 실행한 순서
uv run payload.py
```

과제 풀이:

```bash
cd lessons/14-S2-3/solution
# 녹화에서 실행한 순서
uv run payload.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)

