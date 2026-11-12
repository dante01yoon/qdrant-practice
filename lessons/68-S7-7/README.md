# 68. S7-7 노드를 꺼 보기 — 장애

## 이 수업에서 하는 일

- 노드 하나를 내리면
- 과제 풀이 · 두 대를 내리면

## 파일

- `compose.yaml`
- `failover.py`
- `failover2.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/68-S7-7
# 녹화에서 실행한 순서
uv run failover.py
uv run failover2.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `query_vecs.npy` → `data/query_vecs.npy` (저장소에 들어 있음)

