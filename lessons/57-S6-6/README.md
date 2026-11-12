# 57. S6-6 product와 TurboQuant

## 이 수업에서 하는 일

- product와 TurboQuant
- 과제 풀이 · 같은 크기 비교

## 파일

- `product_turbo.py`
- `quant_helper.py`
- `same_size.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/57-S6-6
# 녹화에서 실행한 순서
uv run product_turbo.py
uv run same_size.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `query_vecs.npy` → `data/query_vecs.npy` (저장소에 들어 있음)
- `vecs_100k.npy` → `data/vecs_100k.npy` (저장소에 없음: `scripts/make_vecs_100k.py (먼저 scripts/embed_titles_all.py)`로 만듭니다)

