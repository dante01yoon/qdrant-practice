# 05. S1-3 왜 Qdrant인가

## 이 수업에서 하는 일

- 거리 방식과 벡터 설정
- 이름 실수
- 메모리 모드
- 과제 풀이

## 파일

- `configs.py`
- `dist_check.py`
- `memory_mode.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/05-S1-3
# 녹화에서 실행한 순서
uv run dist_check.py
uv add qdrant
uv add qdrant-client==1.20.0
uv run memory_mode.py
uv run configs.py
```

