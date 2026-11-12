from qdrant_client import models

from quant_helper import build, no_rescore, recall, run, with_rescore

build(models.TurboQuantization(turbo=models.TurboQuantQuantizationConfig(bits=models.TurboQuantBitSize.BITS4)))
truth, exact_ms = run(models.SearchParams(exact=True))
ignore = models.SearchParams(quantization=models.QuantizationSearchParams(ignore=True))
for name, params in [("양자화 안 씀", ignore), ("rescore 끔", no_rescore()), ("rescore 켬", with_rescore())]:
    got, ms = run(params)
    print(f"{name:10} · recall@10 {recall(got, truth):.3f} · {ms:.1f}ms")
