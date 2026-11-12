# 07. S1-5 Docker로 띄우고 대시보드 둘러보기

## 이 수업에서 하는 일

- 서버가 떠 있는지
- 대시보드 열기
- 컬렉션 목록 표
- products 컬렉션 · Points
- Info 탭
- Memory 탭
- Console 열기
- 콘솔에서 만들기
- 목록에서 확인
- 콘솔에서 지우기
- 이름 오타
- 파이썬으로 같은 일
- 대시보드에서 확인
- 과제 풀이
- Euclid 확인
- 파이썬으로 지우기

## 파일

- `cleanup.py`
- `dashboard_check.py`
- `practice.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/07-S1-5
# 녹화에서 실행한 순서
docker ps --filter name=qdrant --format "{{.Names}}: {{.Status}}"
uv run dashboard_check.py
uv run practice.py
uv run cleanup.py
```

