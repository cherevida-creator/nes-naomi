#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UPSTREAM_COMMIT=e4574b577609a51c6b7ca7914d2f25436831eede
LIBNAOMI_COMMIT=fadc8536d3c115b53277c50dca5d001dfbccc30d
UPSTREAM="$ROOT/vendor/sm64-port-lat"
LIBNAOMI="$ROOT/vendor/libnaomi"
ROM="${SM64_BASEROM:-$ROOT/baserom.us.z64}"

if [[ -z "${KOS_BASE:-}" || ! -f "$KOS_BASE/environ.sh" ]]; then
  echo "ERROR: load the KallistiOS environment first (KOS_BASE/environ.sh)." >&2
  exit 2
fi
if [[ ! -s "$ROM" ]]; then
  echo "ERROR: Super Mario 64 US baserom not found: $ROM" >&2
  echo "Set SM64_BASEROM to a legally obtained baserom.us.z64 file." >&2
  exit 3
fi

mkdir -p "$ROOT/vendor"
if [[ ! -d "$UPSTREAM/.git" ]]; then
  git clone https://github.com/Dreamcast-Projects/sm64-port-lat.git "$UPSTREAM"
fi
if [[ ! -d "$LIBNAOMI/.git" ]]; then
  git clone https://github.com/DragonMinded/libnaomi.git "$LIBNAOMI"
fi
git -C "$UPSTREAM" checkout --detach "$UPSTREAM_COMMIT"
git -C "$LIBNAOMI" checkout --detach "$LIBNAOMI_COMMIT"

ln -sfn "$(realpath "$ROM")" "$UPSTREAM/baserom.us.z64"
python3 "$ROOT/tools/integrate_sm64_naomi.py" --upstream "$UPSTREAM" --libnaomi "$LIBNAOMI" --source "$ROOT"

export KOS_SUBARCH=naomi
make -C "$UPSTREAM" TARGET_DC=1 -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)" elf

NAOMI_BINTOOL="$ROOT/vendor/naomibintool"
cc -O2 -DNO_LIBELF "$KOS_BASE/utils/naomibintool/naomibintool.c" -o "$NAOMI_BINTOOL"
"$NAOMI_BINTOOL" build "$ROOT/mario64-naomi2.bin" \
  -p Naomi2 -d "SM64 Naomi Port" -t "Super Mario 64" \
  -b "$UPSTREAM/build/us_dc/sm64.us.f3dex2e.bin" -s 0x8c020000
"$NAOMI_BINTOOL" read "$ROOT/mario64-naomi2.bin"
sha256sum "$ROOT/mario64-naomi2.bin"
