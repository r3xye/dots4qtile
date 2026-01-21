#!/usr/bin/env bash
set -euo pipefail

entries=$(
  cat <<'EOF'
Brightness +10%
Brightness -10%
EOF
)

if [ "${ROFI_RETV:-0}" -eq 0 ]; then
  printf "%s\n" "$entries"
  exit 0
fi

choice="${1:-}"
case "$choice" in
  "Brightness +10%")
    brightnessctl set +10%
    ;;
  "Brightness -10%")
    brightnessctl set 10%-
    ;;
esac
