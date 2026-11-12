import requests

for port in [6401, 6402, 6403]:
    c = requests.get(f"http://localhost:{port}/cluster").json()["result"]
    print(port, "내 번호", c["peer_id"] % 1000, "· 아는 노드", len(c["peers"]), "· 리더", c["raft_info"]["leader"] % 1000, "· 상태", c["consensus_thread_status"]["consensus_thread_status"])
