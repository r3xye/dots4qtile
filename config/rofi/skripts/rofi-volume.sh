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

get_volume() {
  pactl get-sink-volume @DEFAULT_SINK@ | awk -F'/' 'NR==1 {gsub(/[^0-9]/,"",$2); print $2}'
}

get_mute() {
  pactl get-sink-mute @DEFAULT_SINK@ | awk '{print $2}'
}

vol="$(get_volume)"
mute="$(get_mute)"
vol="${vol:-0}"
bar_text="$(bar "$vol")"
mute_text=""
if [ "$mute" = "yes" ]; then
  mute_text="(muted)"
fi

entries=$(
  cat <<EOF
Level $bar_text ${vol}% $mute_text
Volume +5%
Volume -5%
Set 0%
Set 25%
Set 50%
Set 75%
Set 100%
Mute toggle
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
  "Volume +5%")
    pactl set-sink-volume @DEFAULT_SINK@ +5%
    ;;
  "Volume -5%")
    pactl set-sink-volume @DEFAULT_SINK@ -5%
    ;;
  "Set 0%")
    pactl set-sink-volume @DEFAULT_SINK@ 0%
    ;;
  "Set 25%")
    pactl set-sink-volume @DEFAULT_SINK@ 25%
    ;;
  "Set 50%")
    pactl set-sink-volume @DEFAULT_SINK@ 50%
    ;;
  "Set 75%")
    pactl set-sink-volume @DEFAULT_SINK@ 75%
    ;;
  "Set 100%")
    pactl set-sink-volume @DEFAULT_SINK@ 100%
    ;;
  "Mute toggle")
    pactl set-sink-mute @DEFAULT_SINK@ toggle
    ;;
esac
