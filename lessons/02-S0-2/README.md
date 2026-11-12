# 02. S0-2 실습 환경 준비

## 이 수업에서 하는 일

- 도구 확인
- 서버 띄우기
- -v를 빼먹으면
- 지우고 다시 띄우면
- -v를 붙이면
- 포트 충돌
- 살아 있는지 확인
- 대시보드에서 확인
- 과제 풀이

## 파일

- `check_env.py`
- `env_test.py`
- `list_after.py`
- `no_volume.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/02-S0-2
# 녹화에서 실행한 순서
uv run check_env.py
docker run --name qdrant-demo -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant:v1.20.0
docker rm qdrant-demo
docker run -d --name qdrant-demo -p 6333:6333 qdrant/qdrant:v1.20.0
uv run no_volume.py
docker rm -f qdrant-demo
uv run list_after.py
docker run -d --name qdrant-demo -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant:v1.20.0
ls qdrant_storage
docker run -d --name qdrant-demo2 -p 6333:6333 qdrant/qdrant:v1.20.0
docker rm qdrant-demo2
docker run -d --name qdrant-demo2 -p 6335:6333 qdrant/qdrant:v1.20.0
docker ps --filter name=qdrant --format "{{.Names}}: {{.Status}} {{.Ports}}"
docker rm -f qdrant-demo2
docker logs qdrant-demo 2>&1 | grep listening
uv run env_test.py
```

