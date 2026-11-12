from qdrant_client import models

from quant_helper import build, no_rescore, recall, run, size_mb

truth = None
for quantile in [0.9, 0.99]:
    build(models.ScalarQuantization(scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8, quantile=quantile)))
    truth = truth or run(models.SearchParams(exact=True))[0]
    got, ms = run(no_rescore())
    print(f"quantile {quantile:4} · {size_mb():.0f}MB · recall@10 {recall(got, truth):.3f}")
