#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export NAOMI_BASE="${NAOMI_BASE:-$ROOT/vendor/libnaomi}"

if [ ! -x "$NAOMI_BASE/tools/pyenv/bin/python3" ]; then
  echo "ERROR: libnaomi environment/toolchain is not installed at $NAOMI_BASE" >&2
  echo "Run the libnaomi setup documented in its README first." >&2
  exit 2
fi
if [ ! -d "$ROOT/vendor/nes-core/src" ]; then
  echo "ERROR: NES core missing. Run tools/bootstrap.sh first." >&2
  exit 3
fi
cd "$ROOT"
make clean
make -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)"
test -s nes_naomi.bin
python3 tools/verify_bin.py nes_naomi.bin
