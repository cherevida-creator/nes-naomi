#!/usr/bin/env bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
export SM64_BASEROM='/rom/Super Mario 64 (USA).z64'
export KOS_BASE=/src/vendor/KallistiOS-current
export KOS_SUBARCH=naomi
export KOS_CC_BASE=/opt/toolchains/dc/sh-elf
export KOS_PORTS=/opt/toolchains/dc/kos-ports
mkdir -p "$KOS_PORTS/include" "$KOS_PORTS/lib"
set +u
source "$KOS_BASE/environ.sh"
set -u
KOS_CFLAGS="${KOS_CFLAGS:-}"
KOS_CFLAGS="${KOS_CFLAGS//-D_arch_sub_pristine/-D_arch_sub_naomi}"
export KOS_CFLAGS
KOS_LDFLAGS="$(sed -E \
  -e 's/(^|[[:space:]])-Wl,--defsym=LOAD_OFFSET=[^[:space:]]+//g' \
  -e 's/(^|[[:space:]])-Wl,-Ttext=0x8c[[:xdigit:]]+//g' \
  <<< "${KOS_LDFLAGS:-}")"
KOS_LDFLAGS="${KOS_LDFLAGS} -Wl,--defsym=LOAD_OFFSET=0x8c020000 -Wl,-Ttext=0x8c020000"
export KOS_LDFLAGS
export SM64_PLATFORM_SIGNATURE=NAOMI
export SM64_OUTPUT_BIN=/src/SM64_NAOMI1_COMPAT_EXPERIMENTAL.bin
export KOS_LDFLAGS="$KOS_LDFLAGS -Wl,-Map=/src/SM64_NAOMI1_COMPAT_EXPERIMENTAL.map"
bash /src/tools/build_sm64_naomi2.sh
