from qdrant_client import models

from quant_helper import build, no_rescore, recall, run, with_rescore

build(models.BinaryQuantization(binary=models.BinaryQuantizationConfig()))
truth, exact_ms = run(models.SearchParams(exact=True))
got, ms = run(no_rescore())
print(f"rescore 끔         · recall@10 {recall(got, truth):.3f} · {ms:.1f}ms")
for over in [1.0, 2.0, 4.0, 8.0]:
    got, ms = run(with_rescore(over))
    print(f"oversampling {over:3} · recall@10 {recall(got, truth):.3f} · {ms:.1f}ms")
