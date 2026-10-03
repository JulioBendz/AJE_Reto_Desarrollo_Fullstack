#!/bin/bash
set -euo pipefail
raiz="$(cd "$(dirname "$0")/.." && pwd)"
cd "$raiz"
clave="$(bash "$raiz/scripts/leer-clave-sonar.sh")"
curl -sS -u "admin:$clave" "http://127.0.0.1:9000/api/issues/search?componentKeys=aje-reto-clientes&types=CODE_SMELL&ps=50&resolved=false"
echo
