# 19. S2-8 실패·재시도·이어서 넣기

## 이 수업에서 하는 일

- 다시 시도하고 기록하기
- 서버가 잠깐 꺼지면
- 아예 꺼지면 · 이어서
- 과제 풀이 · 다섯 번 · 10초 상한

## 파일

- `break_at.sh`
- `resume.py`
- `solution/` — 과제 풀이(같은 파일을 고친 버전이라 따로 둠): `break_at.sh`, `resume.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/19-S2-8
# 이 수업용 컨테이너(녹화 전에 띄워 둔 것)
docker run -d --name qdrant-resume -p 127.0.0.1:6450:6333 --memory 1g qdrant/qdrant:v1.20.0

# 녹화에서 실행한 순서
./break_at.sh 3000 restart & uv run resume.py
rm checkpoint.json && curl -s -X DELETE localhost:6450/collections/products_resume > /dev/null
./break_at.sh 3000 stop & uv run resume.py
cat checkpoint.json
docker start qdrant-resume
uv run resume.py
```

과제 풀이:

```bash
cd lessons/19-S2-8/solution
# 이 수업용 컨테이너(녹화 전에 띄워 둔 것)
docker run -d --name qdrant-resume -p 127.0.0.1:6450:6333 --memory 1g qdrant/qdrant:v1.20.0

# 녹화에서 실행한 순서
./break_at.sh 3000 restart & uv run resume.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `product_vecs.npy` → `data/product_vecs.npy` (저장소에 들어 있음)
- `products.parquet` → `data/products.parquet` (저장소에 들어 있음)

