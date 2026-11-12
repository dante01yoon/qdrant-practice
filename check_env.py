import importlib.metadata
import subprocess

uv_ver = subprocess.run(["uv", "--version"], capture_output=True, text=True)
docker_ver = subprocess.run(["docker", "--version"], capture_output=True, text=True)

print("uv 출력:", uv_ver.stdout.strip())
print("docker 출력:", docker_ver.stdout.strip())
print("qdrant-client 버전:", importlib.metadata.version("qdrant-client"))
