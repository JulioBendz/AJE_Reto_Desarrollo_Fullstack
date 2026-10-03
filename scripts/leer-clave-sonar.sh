#!/bin/bash
if [[ -n "${SONAR_ADMIN_PASSWORD:-}" ]]; then
  printf '%s' "$SONAR_ADMIN_PASSWORD"
  exit 0
fi
if [[ -f sonar-admin.local ]]; then
  tr -d '\r\n' < sonar-admin.local
  exit 0
fi
echo "Escribe la clave de admin en sonar-admin.local o exporta SONAR_ADMIN_PASSWORD." >&2
exit 1
