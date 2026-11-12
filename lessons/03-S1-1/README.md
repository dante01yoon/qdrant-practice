# 03. S1-1 복습 ① 벡터·임베딩·거리

## 이 수업에서 하는 일

- 거리 네 가지로 재기
- Cosine이 바꿔 둔 벡터
- 과제 풀이

## 파일

- `euclid_cos.py`
- `four_metrics.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/03-S1-1
# 녹화에서 실행한 순서
uv run four_metrics.py
uv run euclid_cos.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `book_vecs.npy` → `data/book_vecs.npy` (저장소에 들어 있음)

