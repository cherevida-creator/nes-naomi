#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GLDC_COMMIT=f06c72ff145d5354467739f26264160a996e3a2d
GLDC="$ROOT/vendor/GLdc"
BUILD="$ROOT/vendor/GLdc-build-naomi"

if [[ -z "${KOS_BASE:-}" || -z "${KOS_CC_BASE:-}" ]]; then
  echo "ERROR: KOS_BASE and KOS_CC_BASE must point to the KallistiOS SDK and SH-4 toolchain." >&2
  exit 2
fi
command -v cmake >/dev/null || { echo "ERROR: CMake is required to build pinned GLdc." >&2; exit 2; }

if [[ ! -d "$GLDC/.git" ]]; then
  git clone "${GLDC_SOURCE:-https://gitlab.com/simulant/GLdc.git}" "$GLDC"
fi
if ! git -C "$GLDC" cat-file -e "$GLDC_COMMIT^{commit}" 2>/dev/null; then
  git -C "$GLDC" fetch --depth 1 origin "$GLDC_COMMIT"
fi
git -C "$GLDC" checkout --detach "$GLDC_COMMIT"
git -C "$GLDC" reset --hard "$GLDC_COMMIT"

# GLdc's library is C-only. The pinned tree also declares C++-only samples and
# tests, so make the project require only the SH-4 C compiler when building GL.
python3 - "$GLDC/CMakeLists.txt" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
source = path.read_text()
source, project_count = re.subn(
    r"(?m)^project\(GLdc\)$", "project(GLdc C)", source, count=1
)
if project_count != 1:
    raise SystemExit("GLdc CMake project declaration changed; refusing an unverified patch")
source, tests_count = re.subn(r"(?m)^add_subdirectory\(tests\)\s*\n", "", source, count=1)
if tests_count != 1:
    raise SystemExit("GLdc tests declaration changed; refusing an unverified patch")
source, sample_count = re.subn(
    r"(?m)^gen_sample\([^\n]*\.cpp\)\s*\n", "", source
)
if sample_count < 1:
    raise SystemExit("GLdc C++ samples were not found; refusing an unverified patch")
path.write_text(source)
PY

TOOLCHAIN="$ROOT/vendor/kos-gldc-toolchain.cmake"
cat > "$TOOLCHAIN" <<'CMAKE'
set(CMAKE_SYSTEM_NAME Generic)
set(PLATFORM_DREAMCAST TRUE)
if(NOT DEFINED ENV{KOS_BASE} OR NOT DEFINED ENV{KOS_CC_BASE})
  message(FATAL_ERROR "KOS_BASE and KOS_CC_BASE must be set")
endif()
set(KOS_BASE "$ENV{KOS_BASE}")
set(KOS_CC_BASE "$ENV{KOS_CC_BASE}")
if(DEFINED ENV{KOS_PORTS})
  set(KOS_PORTS "$ENV{KOS_PORTS}")
else()
  set(KOS_PORTS "${KOS_BASE}/../kos-ports")
endif()
set(CMAKE_C_COMPILER "${KOS_CC_BASE}/bin/sh-elf-gcc")
set(CMAKE_AR "${KOS_CC_BASE}/bin/sh-elf-ar")
set(CMAKE_RANLIB "${KOS_CC_BASE}/bin/sh-elf-ranlib")
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
set(CMAKE_C_FLAGS_INIT "-O2 -fomit-frame-pointer -D__DREAMCAST__ -D__NAOMI__ -D_arch_dreamcast=1 -D_arch_sub_naomi=1 -DTARGET_DC -DTARGET_NAOMI -I${KOS_BASE}/include -I${KOS_BASE}/kernel/arch/dreamcast/include -I${KOS_BASE}/addons/include -I${KOS_PORTS}/include")
CMAKE

rm -rf "$BUILD"
cmake -S "$GLDC" -B "$BUILD" -G "Unix Makefiles" \
  -DCMAKE_TOOLCHAIN_FILE="$TOOLCHAIN" \
  -DCMAKE_BUILD_TYPE=Release
cmake --build "$BUILD" --target GL --parallel

mkdir -p "$KOS_BASE/addons/include/GL" "$KOS_BASE/addons/lib/dreamcast"
cp "$GLDC"/include/GL/*.h "$KOS_BASE/addons/include/GL/"
cp "$BUILD/libGL.a" "$KOS_BASE/addons/lib/dreamcast/libGL.a"
echo "Installed GLdc $GLDC_COMMIT for KOS Naomi into $KOS_BASE/addons."
