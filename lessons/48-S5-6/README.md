# 48. S5-6 글로 상품 사진 찾기 — 한국어도

## 이 수업에서 하는 일

- 글로 의자 사진 찾기
- 1위 사진 열기
- 러닝화
- 과제 풀이 · 같은 뜻 다른 말

## 파일

- `shoes.py`
- `text_to_image.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/48-S5-6
# 앞 수업에서 만든 상태(컬렉션 등)를 먼저 만들어 둡니다. 앞 수업을 이미 따라왔다면 건너뛰어도 됩니다.
uv run python ../../scripts/warmup/embed_images.py

# 녹화에서 실행한 순서
uv run text_to_image.py
uv run text_to_image.py "running shoes" 러닝화
uv run shoes.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `abo_photos.parquet` → `data/abo_photos.parquet` (저장소에 들어 있음)
- `small` → `data/abo/small` (저장소에 없음: `scripts/prepare_abo.py`로 만듭니다)

