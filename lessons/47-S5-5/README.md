# 47. S5-5 상품 사진을 벡터로 — CLIP

## 이 수업에서 하는 일

- 사진 3,000장을 벡터로
- 과제 풀이 · 짝 표

## 파일

- `embed_images.py`
- `pair_table.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/47-S5-5
# 녹화에서 실행한 순서
uv run embed_images.py
uv run pair_table.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `abo_photos.parquet` → `data/abo_photos.parquet` (저장소에 들어 있음)
- `small` → `data/abo/small` (저장소에 없음: `scripts/prepare_abo.py`로 만듭니다)

