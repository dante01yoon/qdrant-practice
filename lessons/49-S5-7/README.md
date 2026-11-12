# 49. S5-7 사진으로 사진 찾기

## 이 수업에서 하는 일

- 바꾼 사진으로 찾기
- 바꾼 사진 보기
- 과제 풀이 · 다른 종류 사진
- 좋아요와 싫어요로 찾기
- 모든 쌍 비교하기

## 파일

- `duplicates.py`
- `image_to_image.py`
- `more_types.py`
- `recommend.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/49-S5-7
# 앞 수업에서 만든 상태(컬렉션 등)를 먼저 만들어 둡니다. 앞 수업을 이미 따라왔다면 건너뛰어도 됩니다.
uv run python ../../scripts/warmup/embed_images.py

# 녹화에서 실행한 순서
uv run image_to_image.py
uv run more_types.py
uv run recommend.py
uv run duplicates.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `abo_photos.parquet` → `data/abo_photos.parquet` (저장소에 들어 있음)
- `small` → `data/abo/small` (저장소에 없음: `scripts/prepare_abo.py`로 만듭니다)

