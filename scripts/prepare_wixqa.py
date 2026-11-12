# WixQA(MIT, huggingface.co/datasets/Wix/WixQA): 고객센터 글 6,221개(약 54MB) + 전문가 질문 200개를 받는다.
import urllib.request
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"
BASE = "https://huggingface.co/datasets/Wix/WixQA/resolve/main/"
for src, dst in [("wix_kb_corpus/wix_kb_corpus.jsonl", "wix_kb_corpus.jsonl"),
                 ("wixqa_expertwritten/test.jsonl", "wixqa_expertwritten_test.jsonl")]:
    if not (D / dst).exists():
        print("받는 중:", dst, flush=True)
        urllib.request.urlretrieve(BASE + src, D / dst)
print("끝")
