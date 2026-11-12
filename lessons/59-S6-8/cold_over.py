from qdrant_client import models

from quant_helper import N, client, recall, run, vecs, with_rescore
import time

M = models.Memory
if client.collection_exists(N):
    client.delete_collection(N)
client.create_collection(N, vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE, memory=M.COLD),
                         quantization_config=models.TurboQuantization(turbo=models.TurboQuantQuantizationConfig(bits=models.TurboQuantBitSize.BITS4, memory=M.PINNED)))
client.upload_collection(N, vectors=vecs, ids=range(len(vecs)), batch_size=500, wait=True)
while (info := client.get_collection(N)).status != models.CollectionStatus.GREEN or info.indexed_vectors_count < 0.9 * len(vecs):
    time.sleep(0.5)
time.sleep(5)

truth = run(models.SearchParams(exact=True))[0]
for over in [1.0, 2.0, 4.0, 8.0]:
    got, ms = run(with_rescore(over))
    print(f"oversampling {over:3} · recall@10 {recall(got, truth):.3f} · {ms:.1f}ms")
