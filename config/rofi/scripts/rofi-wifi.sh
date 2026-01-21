#!/usr/bin/env bash
set -euo pipefail

if [ "${ROFI_RETV:-0}" -eq 0 ]; then
  nmcli -t -f IN-USE,SSID,SIGNAL dev wifi list | awk -F: '
    $2 == "" { next }
    {
      mark = ($1 == "*") ? " (current)" : ""
      printf "%s [%s%%%]%s\n", $2, $3, mark
    }
  '
  exit 0
fi

choice="${1:-}"
ssid="${choice%% [*}"

if [ -z "$ssid" ]; then
  exit 0
fi

if [[ "$choice" == *"(current)"* ]]; then
  exit 0
fi

if ! nmcli dev wifi connect "$ssid" >/dev/null 2>&1; then
  pass=$(printf "" | rofi -dmenu -password -p "WiFi password")
  if [ -n "$pass" ]; then
    nmcli dev wifi connect "$ssid" password "$pass" >/dev/null 2>&1 || true
  fi
fi
