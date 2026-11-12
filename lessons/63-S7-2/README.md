# 63. S7-2 마켓마다 찾기 — 빠뜨리지 못하게

## 이 수업에서 하는 일

- 마켓마다 따로 찾기
- 과제 풀이 · 빠뜨릴 수 없게

## 파일

- `tenant_guard.py`
- `tenant_search.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/63-S7-2
# 녹화에서 실행한 순서
uv run tenant_search.py
uv run tenant_guard.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `query_vecs.npy` → `data/query_vecs.npy` (저장소에 들어 있음)

