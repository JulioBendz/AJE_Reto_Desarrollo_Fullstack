#!/bin/bash
set -euo pipefail
raiz="$(cd "$(dirname "$0")/.." && pwd)"
cd "$raiz"
base="http://127.0.0.1:9000"
clave="$(bash "$raiz/scripts/leer-clave-sonar.sh")"
curl -sS -u admin:admin -X POST "$base/api/users/change_password?login=admin&previousPassword=admin&password=$clave" || true
echo
token="$(curl -sS -u "admin:$clave" -X POST "$base/api/user_tokens/generate?name=scanner-reto-$(date +%s)")"
echo "$token" > sonar-token.json
python3 - <<'PY'
import json
from pathlib import Path
datos = json.loads(Path("sonar-token.json").read_text(encoding="utf-8"))
Path("sonar-token.local").write_text(datos["token"] + "\n", encoding="utf-8")
print("token-ok")
PY
