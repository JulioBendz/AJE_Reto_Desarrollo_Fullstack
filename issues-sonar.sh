#!/bin/bash
set -euo pipefail
cd /mnt/e/julio-bendezu/AJE_Reto_Desarrollo_Fullstack
clave="RetoLocal1234!"
curl -sS -u "admin:$clave" "http://127.0.0.1:9000/api/issues/search?componentKeys=aje-reto-clientes&types=CODE_SMELL&ps=50&resolved=false"
echo
