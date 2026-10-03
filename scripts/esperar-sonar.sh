#!/bin/bash
set -euo pipefail
raiz="$(cd "$(dirname "$0")/.." && pwd)"
cd "$raiz"
for i in $(seq 1 24); do
  estado="$(curl -sS -m 5 http://127.0.0.1:9000/api/system/status || true)"
  echo "$i $estado"
  if echo "$estado" | grep -q '"status":"UP"'; then
    exit 0
  fi
  sleep 15
done
docker compose -f docker-compose.sonar.yml logs sonarqube --tail 40
exit 1
