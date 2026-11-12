from qdrant_client import models

from quant_helper import build, no_rescore, recall, run, size_mb, with_rescore

scalar = models.ScalarQuantization(scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8))
build(scalar)
truth, exact_ms = run(models.SearchParams(exact=True))
print(f"원래 벡터 391MB → scalar {size_mb():.0f}MB")

got, ms = run(no_rescore())
print(f"rescore 끔 · recall@10 {recall(got, truth):.3f} · {ms:.1f}ms")
got, ms = run(with_rescore())
print(f"rescore 켬 · recall@10 {recall(got, truth):.3f} · {ms:.1f}ms")
