# 실전 벡터 DB: Qdrant로 검색 시스템 만들고 운영하기 — 실습 저장소

강의 「실전 벡터 DB: Qdrant로 검색 시스템 만들고 운영하기」(90개 수업)의 실습 코드와 데이터입니다.
수업 폴더마다 그 수업이 끝났을 때의 코드가 그대로 들어 있습니다.

- Qdrant 1.20.0 (Docker) · qdrant-client 1.20.0 · Python 3.11~3.12
- 패키지 관리: [uv](https://docs.astral.sh/uv/)

## 1. 준비

```bash
git clone https://github.com/dante01yoon/qdrant-practice.git
cd qdrant-practice
uv sync                        # pyproject.toml + uv.lock 그대로 설치(qdrant-client==1.20.0)
uv run python check_env.py     # uv·Docker·qdrant-client 버전 확인
```

`check_env.py`에서 Docker 데몬에 연결할 수 없다고 나오면 Docker Desktop 앱부터 켜 두세요.

## 2. Qdrant 서버 띄우기

강의 전체에서 쓰는 서버입니다. 저장소 폴더에서 실행하면 데이터가 `qdrant_storage/`에 남아서 컨테이너를 지워도 사라지지 않습니다.

```bash
docker run -d --name qdrant-course -p 6333:6333 -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant:v1.20.0
```

- 대시보드: http://localhost:6333/dashboard
- 멈추기·다시 켜기: `docker stop qdrant-course` / `docker start qdrant-course`
- 컨테이너 이름은 `qdrant-course`로 맞춰 주세요. 몇몇 수업 코드가 이 이름으로 `docker exec`을 합니다.
- S0-2 수업에서는 연습용으로 `qdrant-demo` 컨테이너를 따로 띄웠다 지웁니다.

### pgvector 컨테이너 (S3-8, 섹션 8)

```bash
docker run -d --name qdrant-course-pg -e POSTGRES_PASSWORD=course -p 5434:5432 pgvector/pgvector:0.8.1-pg17
```

수업 코드는 `postgresql://postgres:course@localhost:5434/postgres`로 접속합니다(실습 전용 비밀번호).

몇몇 수업(S2-8, S6-9, S6-10, 섹션 7 클러스터, S8-5 OpenSearch, S9-7 compose)은 코드나 README 안의 명령으로 실습용 컨테이너를 따로 띄우고 지웁니다. 각 수업 README를 보세요.

## 3. 데이터

### 저장소에 들어 있는 것 (`data/`, 약 145MB)

| 파일 | 내용 |
|---|---|
| `products.parquet` | 아마존 ESCI 미국 상품 10,017개(상품명·설명·특징·브랜드·색상) |
| `product_vecs.npy` | 위 상품의 bge-m3 벡터(10,017 × 1,024). **컴퓨터가 느리면 임베딩을 건너뛰고 이 파일을 쓰면 됩니다** |
| `queries.csv`, `query_vecs.npy` | 실제 검색어 500개와 그 벡터 |
| `qrels.csv` | 사람이 매긴 정답(E 정확·S 대체품·C 함께 쓰는 상품·I 무관) 10,158줄 |
| `title_vecs.npy`, `detail_vecs.npy` | 상품명만·특징만 벡터(이름 붙인 벡터 실습) |
| `market_products.parquet`, `market_qrels.csv`, `market_vecs.npy` | 스페인·일본 상품(권한 필터·멀티테넌시 실습) |
| `book_vecs.npy` | 복습 수업(S1-1)용 책 소개 벡터 1,307개 |
| `abo_photos.parquet` | 사진 검색 실습용 ABO 상품 3,000개 목록(사진은 아래 스크립트로 받음) |
| `shop_vocab.json`, `wix_vocab.json` | BM25 단어 사전(섹션 4·9) |

수업 폴더 안의 데이터 파일은 `data/`를 가리키는 바로가기(symlink)입니다. 수업 폴더에서 바로 `uv run` 하면 됩니다.
Windows에서는 `git clone -c core.symlinks=true ...`로 받거나, 필요한 파일을 `data/`에서 수업 폴더로 복사하세요.

### 스크립트로 만드는 것 (용량이 커서 저장소에 넣지 않음)

| 스크립트 | 만드는 것 | 쓰는 수업 |
|---|---|---|
| `uv run python scripts/prepare_esci.py` | ESCI 원본(약 1.2GB, `data/raw/`)을 받아 `products.parquet`·`qrels.csv`·`queries.csv`를 다시 만듦(`--raw-only`면 원본만) | S2-0 |
| `uv run python scripts/embed_esci.py` (`named`) | `product_vecs.npy`·`query_vecs.npy` (`title_vecs`·`detail_vecs`)를 직접 임베딩 | 직접 만들어 보고 싶을 때 |
| `uv run python scripts/prepare_markets.py` | `market_*` 파일 다시 만들기 | 직접 만들어 보고 싶을 때 |
| `uv run python scripts/embed_titles_all.py [개수]` | 미국 상품 121만 개 상품명 벡터(`data/esci_us_titles/`, 5만 개씩, 약 5GB, 몇 시간) | S3-5(10만), S6-9·S6-10(121만) |
| `uv run python scripts/make_vecs_100k.py` | `vecs_100k.npy`(위 결과 앞 10만 개) | S6-1~S6-8, S8-2 |
| `uv run python scripts/make_colbert.py` | ColBERT 토큰 벡터(`colbert_*.npy`, 약 420MB) | S5-3·S5-4 |
| `uv run python scripts/prepare_wixqa.py` | WixQA 고객센터 글·질문(`wix_kb_corpus.jsonl`·`wixqa_expertwritten_test.jsonl`) | S2-9, S4-10, S4-12, S9-1, S9-2, S9-6 |
| `uv run python scripts/build_wix_full.py` | `wix_full` 컬렉션(WixQA 글 전체를 조각내 임베딩) | S2-9(`ask.py`), S4-12 |
| `uv run python scripts/make_wix_snapshot.py` | `wix_hybrid.snapshot`(S4-12 `wix_build.py` 뒤에) | S9-3, S9-7 |
| `uv run python scripts/prepare_abo.py` | ABO 상품 사진 3,000장(`data/abo/small/`) | S5-5~S5-9 |

### 중간 수업부터 시작할 때

수업은 앞 수업에서 만든 컬렉션을 이어 씁니다. 중간부터 시작한다면 그 수업 README의 「앞 수업에서 만든 상태」 명령(`scripts/warmup/`)을 먼저 돌리세요. 수업 폴더 안에서 실행합니다.

## 4. 폴더

```
check_env.py          S0-2 환경 확인
pyproject.toml, uv.lock
data/                 실습 데이터(위 표)
scripts/              데이터 받기·만들기
scripts/warmup/       앞 수업 상태를 한 번에 만드는 스크립트
lessons/NN-ID/        수업별 코드(NN = 강의 순서, ID = 수업 번호)
```

`solution/`이 있는 수업은 과제 풀이에서 본편 파일을 고쳐 썼기 때문에 풀이 버전을 따로 둔 것입니다.

| 폴더 | 수업 | 비고 |
|---|---|---|
| [01-S0-1](lessons/01-S0-1) | 강의 소개 — 무엇을 만들고 무엇을 할 수 있게 되나 | 개념 수업(코드 없음) |
| [02-S0-2](lessons/02-S0-2) | 실습 환경 준비 |  |
| [03-S1-1](lessons/03-S1-1) | 복습 ① 벡터·임베딩·거리 |  |
| [04-S1-2](lessons/04-S1-2) | 복습 ② HNSW·필터·하이브리드 |  |
| [05-S1-3](lessons/05-S1-3) | 왜 Qdrant인가 |  |
| [06-S1-4](lessons/06-S1-4) | Qdrant 구조 한 장 |  |
| [07-S1-5](lessons/07-S1-5) | Docker로 띄우고 대시보드 둘러보기 |  |
| [08-S1-6](lessons/08-S1-6) | 파이썬 클라이언트로 첫 검색 |  |
| [09-S1-7](lessons/09-S1-7) | REST·gRPC로 같은 검색 |  |
| [10-S1-8](lessons/10-S1-8) | 과제·풀이 |  |
| [11-S2-0](lessons/11-S2-0) | 실습 데이터 준비: 아마존 ESCI |  |
| [12-S2-1](lessons/12-S2-1) | 컬렉션 설정(차원·거리) |  |
| [13-S2-2](lessons/13-S2-2) | 포인트 ID 설계 |  |
| [14-S2-3](lessons/14-S2-3) | payload 설계 |  |
| [15-S2-4](lessons/15-S2-4) | 이름 붙인 벡터 |  |
| [16-S2-5](lessons/16-S2-5) | upsert와 다시 돌려도 안전한 적재 |  |
| [17-S2-6](lessons/17-S2-6) | 고치기·지우기·payload만 바꾸기 |  |
| [18-S2-7](lessons/18-S2-7) | 배치 적재와 속도 실측 |  |
| [19-S2-8](lessons/19-S2-8) | 실패·재시도·이어서 넣기 |  |
| [20-S2-9](lessons/20-S2-9) | 청킹·메타데이터 적재 파이프라인 |  |
| [21-S2-10](lessons/21-S2-10) | 과제·풀이 |  |
| [22-S3-1](lessons/22-S3-1) | 필터 문법(must·should·must_not) |  |
| [23-S3-2](lessons/23-S3-2) | 범위·목록·제외·빈 값 조건 |  |
| [24-S3-3](lessons/24-S3-3) | payload 인덱스 종류 |  |
| [25-S3-4](lessons/25-S3-4) | 인덱스 있을 때와 없을 때 실측 |  |
| [26-S3-5](lessons/26-S3-5) | 필터는 검색 중에 걸린다 — 원리와 10만 개 실측 |  |
| [27-S3-7](lessons/27-S3-7) | 아주 좁은 필터 |  |
| [28-S3-8](lessons/28-S3-8) | pgvector iterative scan과 나란히 |  |
| [29-S3-9](lessons/29-S3-9) | 마켓 필터를 빼먹으면 |  |
| [30-S3-10](lessons/30-S3-10) | 과제·풀이 |  |
| [31-S4-1](lessons/31-S4-1) | sparse 벡터란 |  |
| [32-S4-2](lessons/32-S4-2) | BM25를 sparse로 |  |
| [33-S4-3](lessons/33-S4-3) | 토큰 나누기와 한국어 질문 |  |
| [34-S4-4](lessons/34-S4-4) | dense와 sparse를 한 컬렉션에 |  |
| [35-S4-5](lessons/35-S4-5) | Query API와 prefetch |  |
| [36-S4-6](lessons/36-S4-6) | RRF로 섞기 |  |
| [37-S4-7](lessons/37-S4-7) | DBSF와 다섯 가지 비교 |  |
| [38-S4-8](lessons/38-S4-8) | 가중치와 여러 단계 검색 |  |
| [39-S4-9](lessons/39-S4-9) | 리랭커로 다시 채점하기 |  |
| [40-S4-10](lessons/40-S4-10) | 평가셋 넓히기 — 고른 방법 다시 확인 |  |
| [41-S4-11](lessons/41-S4-11) | 질문별 분석 — 언제 이기고 지나 |  |
| [42-S4-12](lessons/42-S4-12) | 과제 — 고객센터 하이브리드 만들기 |  |
| [43-S5-1](lessons/43-S5-1) | 상품명·특징 벡터 따로 두고 섞기 |  |
| [44-S5-2](lessons/44-S5-2) | 멀티벡터(늦은 상호작용) 개념 |  |
| [45-S5-3](lessons/45-S5-3) | ColBERT로 상품 다시 매기기 |  |
| [46-S5-4](lessons/46-S5-4) | ColBERT의 비용 실측 |  |
| [47-S5-5](lessons/47-S5-5) | 상품 사진을 벡터로 — CLIP |  |
| [48-S5-6](lessons/48-S5-6) | 글로 상품 사진 찾기 — 한국어도 |  |
| [49-S5-7](lessons/49-S5-7) | 사진으로 사진 찾기 |  |
| [50-S5-8](lessons/50-S5-8) | 글과 사진을 섞은 검색 화면 |  |
| [51-S5-9](lessons/51-S5-9) | 과제 — 검색 화면에 종류 고르기 |  |
| [52-S6-1](lessons/52-S6-1) | 메모리는 얼마나 드나 — 계산과 실측 |  |
| [53-S6-2](lessons/53-S6-2) | HNSW 그래프 — m과 ef_construct |  |
| [54-S6-3](lessons/54-S6-3) | 검색할 때 정하는 hnsw_ef |  |
| [55-S6-4](lessons/55-S6-4) | scalar 양자화 — 4분의 1로 |  |
| [56-S6-5](lessons/56-S6-5) | binary 양자화 — 32분의 1로 |  |
| [57-S6-6](lessons/57-S6-6) | product와 TurboQuant |  |
| [58-S6-7](lessons/58-S6-7) | rescore와 oversampling |  |
| [59-S6-8](lessons/59-S6-8) | 벡터를 디스크로 — 메모리 계층 |  |
| [60-S6-9](lessons/60-S6-9) | 미국 상품 121만 개로 재 보기 |  |
| [61-S6-10](lessons/61-S6-10) | 과제 — 메모리를 어디까지 줄일 수 있나 |  |
| [62-S7-1](lessons/62-S7-1) | 한 컬렉션에 여러 마켓 — 멀티테넌시 |  |
| [63-S7-2](lessons/63-S7-2) | 마켓마다 찾기 — 빠뜨리지 못하게 |  |
| [64-S7-3](lessons/64-S7-3) | 컬렉션을 나누면 — 비용 비교 |  |
| [65-S7-4](lessons/65-S7-4) | 노드 세 대 띄우기 |  |
| [66-S7-5](lessons/66-S7-5) | 샤드 — 데이터 나누기 |  |
| [67-S7-6](lessons/67-S7-6) | 복제 — 사본 두기 |  |
| [68-S7-7](lessons/68-S7-7) | 노드를 꺼 보기 — 장애 |  |
| [69-S7-8](lessons/69-S7-8) | 스냅샷 — 백업 만들기 |  |
| [70-S7-9](lessons/70-S7-9) | 복구 — 지우고 되살리기 |  |
| [71-S7-10](lessons/71-S7-10) | 모니터링 — 상태 살피기 |  |
| [72-S7-11](lessons/72-S7-11) | 모델 교체 ① — 새 컬렉션과 별칭 |  |
| [73-S7-12](lessons/73-S7-12) | 모델 교체 ② — 멈추지 않고 바꾸기 |  |
| [74-S7-13](lessons/74-S7-13) | 업그레이드와 용량 계획 |  |
| [75-S7-14](lessons/75-S7-14) | 과제 — 세 마켓을 세 대에 |  |
| [76-S8-1](lessons/76-S8-1) | pgvector로 같은 상품 찾기 |  |
| [77-S8-2](lessons/77-S8-2) | 10만 개로 성능 비교 |  |
| [78-S8-3](lessons/78-S8-3) | 필터와 하이브리드 — 차이가 나는 곳 |  |
| [79-S8-4](lessons/79-S8-4) | 운영 — 이미 있는 것과 새로 들이는 것 |  |
| [80-S8-5](lessons/80-S8-5) | OpenSearch — 검색 엔진에서 온 벡터 |  |
| [81-S8-6](lessons/81-S8-6) | 결정표 — 언제 무엇을 고를까 | 개념 수업(코드 없음) |
| [82-S8-7](lessons/82-S8-7) | 과제 풀이 — recall을 맞춰 놓고 비교 |  |
| [83-S9-1](lessons/83-S9-1) | 무엇을 만들까 — 요구사항과 데이터 |  |
| [84-S9-2](lessons/84-S9-2) | 어떻게 만들까 — 숫자로 설계하기 |  |
| [85-S9-3](lessons/85-S9-3) | 데이터 넣기 — 다시 돌려도 안전하게 |  |
| [86-S9-4](lessons/86-S9-4) | 검색 API — 다른 프로그램이 부를 수 있게 |  |
| [87-S9-5](lessons/87-S9-5) | 화면 — 손님이 쓰는 모습으로 |  |
| [88-S9-6](lessons/88-S9-6) | 평가와 성적표 — 끝났다고 말할 근거 |  |
| [89-S9-7](lessons/89-S9-7) | 배포 — 컨테이너로 묶어서 띄우기 |  |
| [90-S9-8](lessons/90-S9-8) | 돌아보기와 다음 단계 | 개념 수업(코드 없음) |

## 데이터 출처와 라이선스

- Amazon ESCI Shopping Queries Dataset — Apache License 2.0, https://github.com/amazon-science/esci-data (Reddy et al., 2022, "Shopping Queries Dataset: A Large-Scale ESCI Benchmark for Improving Product Search")
- WixQA — MIT License, https://huggingface.co/datasets/Wix/WixQA
- Amazon Berkeley Objects (ABO) — CC BY 4.0, https://amazon-berkeley-objects.s3.amazonaws.com/index.html (Collins et al., 2022)
- `book_vecs.npy` — 한국어 위키백과 책 문서 소개글(CC BY-SA 4.0)을 bge-m3로 바꾼 벡터
- 임베딩 모델: BAAI/bge-m3 (MIT), answerdotai/answerai-colbert-small-v1 (Apache-2.0), clip-ViT-B-32
