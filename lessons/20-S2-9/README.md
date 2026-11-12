# 20. S2-9 청킹·메타데이터 적재 파이프라인

## 이 수업에서 하는 일

- 파이프라인 짜기
- 300개 글로 돌려 보기
- 조각 번호를 ID에
- 질문으로 찾아보기
- 과제 풀이 · 알려진 문제만

## 파일

- `ask.py`
- `ask_type.py`
- `embed.py`
- `pipeline.py`

수업이 끝났을 때의 모습 그대로입니다(녹화에서 직접 입력한 코드).

## 실행

저장소 루트에서 `uv sync`를 한 번 해 두고, Qdrant 서버(localhost:6333)를 켠 뒤 이 폴더에서 실행합니다.

```bash
cd lessons/20-S2-9
# 녹화에서 실행한 순서
uv run pipeline.py 300
curl -s -X DELETE localhost:6333/collections/wix_chunks > /dev/null && uv run pipeline.py 300
uv run ask.py
uv run ask_type.py
```

## 쓰는 데이터

큰 데이터 파일은 저장소 `data/`를 가리키는 바로가기(symlink)입니다. Windows에서는 `git clone -c core.symlinks=true`로 받거나, `data/`의 파일을 이 폴더에 복사해서 쓰세요.

- `wix_kb_corpus.jsonl` → `data/wix_kb_corpus.jsonl` (저장소에 없음: `scripts/prepare_wixqa.py`로 만듭니다)

