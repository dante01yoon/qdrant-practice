# 11. S2-0 실습 데이터 준비: 아마존 ESCI

## 이 수업에서 하는 일

- 채점표 받기
- 채점표 열어 보기
- 한 줄씩 읽기
- 잘라 내기 코드
- 잘라 낸 결과
- 상품을 글 한 덩어리로
- 빈 칸 고치고 임베딩

## 파일

- `embed.py`
- `look.py`
- `prepare.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/11-S2-0
# 녹화에서 실행한 순서
curl -L -o raw/shopping_queries_dataset_examples.parquet https://github.com/amazon-science/esci-data/raw/main/shopping_queries_dataset/shopping_queries_dataset_examples.parquet
du -h raw/*
uv run look.py
uv run prepare.py
uv run embed.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)
- `qrels.csv` → `data/qrels.csv` (저장소에 들어 있음)
- `raw` → `data/raw` (저장소에 없음: `scripts/prepare_esci.py --raw-only`로 만듭니다)

