import requests

U = "http://localhost:6333"
print("healthz", requests.get(f"{U}/healthz").status_code, "· readyz", requests.get(f"{U}/readyz").status_code)

lines = requests.get(f"{U}/metrics").text.splitlines()
values = [l for l in lines if not l.startswith("#")]
print("지표 줄", len(values))
for want in ["app_info", "collections_total", "collections_vector_total", "rest_responses_total", "rest_responses_duration_seconds_count", "memory_resident_bytes"]:
    hit = [l for l in values if l.startswith(want)]
    print(want, "·", hit[0][:70] if hit else "없음")
