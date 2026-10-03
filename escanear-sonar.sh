#!/bin/bash
set -euo pipefail
cd /mnt/e/julio-bendezu/AJE_Reto_Desarrollo_Fullstack
token="$(tr -d '\r\n' < sonar-token.local)"
docker run --rm --network host \
  -e SONAR_HOST_URL=http://127.0.0.1:9000 \
  -e SONAR_TOKEN="$token" \
  -v /mnt/e/julio-bendezu/AJE_Reto_Desarrollo_Fullstack:/usr/src \
  sonarsource/sonar-scanner-cli
