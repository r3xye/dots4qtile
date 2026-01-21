#!/usr/bin/env bash
set -euo pipefail

bar() {
  local percent="$1"
  local total=10
  local filled=$((percent * total / 100))
  local empty=$((total - filled))
  printf "%0.s#" $(seq 1 "$filled")
  printf "%0.s." $(seq 1 "$empty")
}

get_brightness() {
  brightnessctl -m info | awk -F',' '{gsub(/%/,"",$4); print $4}'
}

bright="$(get_brightness)"
bright="${bright:-0}"
bar_text="$(bar "$bright")"

entries=$(
  cat <<EOF
Level $bar_text ${bright}%
Brightness +10%
Brightness -10%
Set 0%
Set 25%
Set 50%
Set 75%
Set 100%
EOF
)

if [ "${ROFI_RETV:-0}" -eq 0 ]; then
  printf "%s\n" "$entries"
  exit 0
fi

choice="${1:-}"
case "$choice" in
  "Level "*)
    exit 0
    ;;
  "Brightness +10%")
    brightnessctl set +10%
    ;;
  "Brightness -10%")
    brightnessctl set 10%-
    ;;
  "Set 0%")
    brightnessctl set 0%
    ;;
  "Set 25%")
    brightnessctl set 25%
    ;;
  "Set 50%")
    brightnessctl set 50%
    ;;
  "Set 75%")
    brightnessctl set 75%
    ;;
  "Set 100%")
    brightnessctl set 100%
    ;;
esac
