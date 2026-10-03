#!/bin/bash
set -euo pipefail
cd /mnt/e/julio-bendezu/AJE_Reto_Desarrollo_Fullstack
clave="RetoLocal1234!"
curl -sS -u "admin:$clave" "http://127.0.0.1:9000/api/qualitygates/project_status?projectKey=aje-reto-clientes"
echo
curl -sS -u "admin:$clave" "http://127.0.0.1:9000/api/measures/component?component=aje-reto-clientes&metricKeys=coverage,bugs,vulnerabilities,code_smells,duplicated_lines_density,security_hotspots,ncloc"
echo
