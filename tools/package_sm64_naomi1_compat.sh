#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ELF="$ROOT/vendor/sm64-port-lat/build/us_dc/sm64.us.f3dex2e"
RAW="$ELF.bin"
READELF="${SM64_READELF:-/home/david/dc-sh-toolchain/bin/sh-elf-readelf}"
LOAD="$("$READELF" -lW "$ELF" | awk '$1=="LOAD"{print $3;exit}')"
ENTRY="$("$READELF" -h "$ELF" | awk '/Entry point address:/{print $NF}')"
test "$LOAD" = 0x8c020000
test "$ENTRY" = 0x8c020000
"$ROOT/vendor/naomibintool" build "$ROOT/SM64_NAOMI1_COMPAT_EXPERIMENTAL.bin" -p NAOMI -d "SM64 Native Port" -t "Super Mario 64" -b "$RAW:$LOAD" -s "$ENTRY"
"$ROOT/vendor/naomibintool" read "$ROOT/SM64_NAOMI1_COMPAT_EXPERIMENTAL.bin"
sha256sum "$ROOT/SM64_NAOMI1_COMPAT_EXPERIMENTAL.bin"
