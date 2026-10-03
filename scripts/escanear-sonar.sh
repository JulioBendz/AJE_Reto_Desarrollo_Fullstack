#!/bin/bash
set -euo pipefail
raiz="$(cd "$(dirname "$0")/.." && pwd)"
cd "$raiz"
token="$(tr -d '\r\n' < sonar-token.local)"
docker run --rm --network host \
  -e SONAR_HOST_URL=http://127.0.0.1:9000 \
  -e SONAR_TOKEN="$token" \
  -v "$raiz":/usr/src \
  sonarsource/sonar-scanner-cli
