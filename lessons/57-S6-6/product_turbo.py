from qdrant_client import models

from quant_helper import build, no_rescore, recall, run, size_mb, with_rescore

turbo = lambda bits: models.TurboQuantization(turbo=models.TurboQuantQuantizationConfig(bits=bits))
B = models.TurboQuantBitSize
WAYS = {
    "product x16": models.ProductQuantization(product=models.ProductQuantizationConfig(compression=models.CompressionRatio.X16)),
    "turbo bits4": turbo(B.BITS4),
    "turbo bits2": turbo(B.BITS2),
}
truth = None
for name, quant in WAYS.items():
    build(quant)
    truth = truth or run(models.SearchParams(exact=True))[0]
    plain = recall(run(no_rescore())[0], truth)
    print(f"{name:12} · {size_mb():.0f}MB · rescore 끔 {plain:.3f} · 켬 {recall(run(with_rescore())[0], truth):.3f}")
