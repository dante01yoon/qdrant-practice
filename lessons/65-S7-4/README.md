# 65. S7-4 노드 세 대 띄우기

## 이 수업에서 하는 일

- compose 파일 쓰고 띄우기
- 노드끼리 서로 아는지 확인

## 파일

- `cluster_check.py`
- `compose.yaml`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/65-S7-4
# 녹화에서 실행한 순서
docker compose -p qdcluster up -d
uv run cluster_check.py
```

