#!/usr/bin/env bash
set -euo pipefail

entries=$(
  cat <<'EOF'
Volume +5%
Volume -5%
Mute toggle
EOF
)

if [ "${ROFI_RETV:-0}" -eq 0 ]; then
  printf "%s\n" "$entries"
  exit 0
fi

choice="${1:-}"
case "$choice" in
  "Volume +5%")
    pactl set-sink-volume @DEFAULT_SINK@ +5%
    ;;
  "Volume -5%")
    pactl set-sink-volume @DEFAULT_SINK@ -5%
    ;;
  "Mute toggle")
    pactl set-sink-mute @DEFAULT_SINK@ toggle
    ;;
esac
