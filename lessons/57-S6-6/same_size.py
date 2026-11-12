from qdrant_client import models

from quant_helper import build, no_rescore, recall, run, size_mb, with_rescore

WAYS = {
    "binary two_bits": models.BinaryQuantization(binary=models.BinaryQuantizationConfig(encoding=models.BinaryQuantizationEncoding.TWO_BITS)),
    "turbo bits2": models.TurboQuantization(turbo=models.TurboQuantQuantizationConfig(bits=models.TurboQuantBitSize.BITS2)),
}
truth = None
for name, quant in WAYS.items():
    build(quant)
    truth = truth or run(models.SearchParams(exact=True))[0]
    plain = recall(run(no_rescore())[0], truth)
    print(f"{name:16} · {size_mb():.0f}MB · rescore 끔 {plain:.3f} · 켬 {recall(run(with_rescore())[0], truth):.3f}")
