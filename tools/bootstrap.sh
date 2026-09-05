#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIBNAOMI_COMMIT=fb6f6e3f42885ddb845977392fad8f5a9bfa7ad5
NES_CORE_COMMIT=69e433da8bd1eaf993659991f30b4989b77dad2c

mkdir -p "$ROOT/vendor"
if [ ! -d "$ROOT/vendor/nes-core/.git" ]; then
  git clone https://github.com/PeakRacing/nes.git "$ROOT/vendor/nes-core"
fi
git -C "$ROOT/vendor/nes-core" fetch --all --tags
git -C "$ROOT/vendor/nes-core" checkout "$NES_CORE_COMMIT"

if [ ! -d "$ROOT/vendor/libnaomi/.git" ]; then
  git clone https://github.com/DragonMinded/libnaomi.git "$ROOT/vendor/libnaomi"
fi
git -C "$ROOT/vendor/libnaomi" fetch --all --tags
git -C "$ROOT/vendor/libnaomi" checkout "$LIBNAOMI_COMMIT"

echo "Sources pinned. Next: build/install libnaomi toolchain, then run tools/build.sh"
