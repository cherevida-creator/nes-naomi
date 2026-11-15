#!/usr/bin/env bash
set -euo pipefail
export SM64_NAOMI_RUNTIME_EXPERIMENTAL=1
export SM64_OUTPUT_BIN="${SM64_OUTPUT_BIN:-/src/SM64_NAOMI_GRAPHICS_SAVE_EXPERIMENTAL.bin}"
bash "$(cd "$(dirname "$0")" && pwd)/build_sm64_graphics.sh"