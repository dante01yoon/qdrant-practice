from qdrant_client import models

from quant_helper import build, recall, run, with_rescore

build(models.TurboQuantization(turbo=models.TurboQuantQuantizationConfig(bits=models.TurboQuantBitSize.BITS2)))
truth, exact_ms = run(models.SearchParams(exact=True))
for over in [1.0, 2.0, 4.0]:
    got, ms = run(with_rescore(over))
    per = [len(g & t) / 10 for g, t in zip(got, truth)]
    print(f"bits2 · oversampling {over:3} · 평균 {recall(got, truth):.3f} · 가장 나쁜 질문 {min(per):.1f} · {ms:.1f}ms")
