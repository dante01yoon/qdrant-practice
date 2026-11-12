#!/bin/zsh
# 실습용: 기록 파일의 next가 $1에 닿으면 서버를 끈다. restart면 4초 뒤 다시 켠다
until [[ -f checkpoint.json ]] && (( $(python3 -c "import json; print(json.load(open('checkpoint.json'))['next'])") >= $1 )); do sleep 0.05; done
if [[ $2 == restart ]]; then docker stop -t 0 qdrant-resume > /dev/null; sleep 4; docker start qdrant-resume > /dev/null; else docker stop -t 0 qdrant-resume > /dev/null; fi
