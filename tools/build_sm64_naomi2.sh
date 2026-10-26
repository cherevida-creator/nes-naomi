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
git -C "$UPSTREAM" reset --hard "$UPSTREAM_COMMIT"
git -C "$LIBNAOMI" reset --hard "$LIBNAOMI_COMMIT"

export KOS_SUBARCH=naomi
KOS_CFLAGS="${KOS_CFLAGS:-}"
KOS_CFLAGS="${KOS_CFLAGS//-D_arch_sub_pristine/-D_arch_sub_naomi}"
export KOS_CFLAGS
bash "$ROOT/tools/build_gldc_naomi.sh"

ln -sfn "$(realpath "$ROM")" "$UPSTREAM/baserom.us.z64"
python3 "$ROOT/tools/integrate_sm64_naomi.py" --upstream "$UPSTREAM" --libnaomi "$LIBNAOMI" --source "$ROOT"

make -C "$UPSTREAM" TARGET_DC=1 -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)" elf

NAOMI_BINTOOL_SOURCE="$ROOT/vendor/naomibintool-naomi2.c"
cp "$KOS_BASE/utils/naomibintool/naomibintool.c" "$NAOMI_BINTOOL_SOURCE"
python3 - "$NAOMI_BINTOOL_SOURCE" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
source = path.read_text()
before = "strtoul(tmp2, NULL, 16);"
if source.count(before) != 1:
    raise SystemExit("naomibintool load-address parser changed; refusing an unverified patch")
path.write_text(source.replace(before, "strtoul(tmp2 + 1, NULL, 16);", 1))
PY
NAOMI_BINTOOL="$ROOT/vendor/naomibintool"
cc -O2 -DNO_LIBELF "$NAOMI_BINTOOL_SOURCE" -o "$NAOMI_BINTOOL"
ELF="$UPSTREAM/build/us_dc/sm64.us.f3dex2e"
BIN="$ELF.bin"
LOAD_ADDRESS="$("$KOS_CC_BASE/bin/sh-elf-readelf" -lW "$ELF" | awk '$1 == "LOAD" { print $3; exit }')"
ENTRY_POINT="$("$KOS_CC_BASE/bin/sh-elf-readelf" -h "$ELF" | awk '/Entry point address:/ { print $NF }')"
if [[ -z "$LOAD_ADDRESS" || -z "$ENTRY_POINT" ]]; then
  echo "ERROR: could not determine the SH-4 ELF load address and entry point." >&2
  exit 4
fi
"$NAOMI_BINTOOL" build "$ROOT/mario64-naomi2.bin" \
  -p Naomi2 -d "SM64 Naomi Port" -t "Super Mario 64" \
  -b "$BIN:$LOAD_ADDRESS" -s "$ENTRY_POINT"
"$NAOMI_BINTOOL" read "$ROOT/mario64-naomi2.bin"
HEADER_INFO="$("$NAOMI_BINTOOL" read "$ROOT/mario64-naomi2.bin")"
grep -q "RAM Offset: ${LOAD_ADDRESS#0x}" <<<"$HEADER_INFO"
grep -q "Entry point: ${ENTRY_POINT#0x}" <<<"$HEADER_INFO"
sha256sum "$ROOT/mario64-naomi2.bin"
