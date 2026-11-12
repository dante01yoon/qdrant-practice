from qdrant_client import models

from quant_helper import build, no_rescore, recall, run, size_mb, with_rescore

E = models.BinaryQuantizationEncoding
truth = None
for encoding in [E.ONE_BIT, E.ONE_AND_HALF_BITS, E.TWO_BITS]:
    build(models.BinaryQuantization(binary=models.BinaryQuantizationConfig(encoding=encoding)))
    truth = truth or run(models.SearchParams(exact=True))[0]
    plain = recall(run(no_rescore())[0], truth)
    print(f"{encoding.value:18} · {size_mb():.0f}MB · rescore 끔 {plain:.3f} · 켬 {recall(run(with_rescore())[0], truth):.3f}")
