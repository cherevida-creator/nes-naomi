#!/usr/bin/env python3
"""Apply Naomi controls and a KOS/JVS bridge to pinned upstream trees."""
import argparse
import shutil
import subprocess
from pathlib import Path

UPSTREAM_COMMIT = "e4574b577609a51c6b7ca7914d2f25436831eede"
LIBNAOMI_COMMIT = "fadc8536d3c115b53277c50dca5d001dfbccc30d"


def replace_once(source: str, before: str, after: str, label: str) -> str:
    count = source.count(before)
    if count != 1:
        raise SystemExit(f"expected one {label} insertion point, found {count}")
    return source.replace(before, after, 1)


def replace_all(source: str, before: str, after: str, label: str) -> str:
    if before not in source:
        raise SystemExit(f"missing {label} replacement point")
    return source.replace(before, after)


def checked_revision(repo: Path, expected: str, label: str) -> None:
    actual = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if actual != expected:
        raise SystemExit(f"{label} revision mismatch: expected {expected}, got {actual}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", required=True, type=Path)
    parser.add_argument("--libnaomi", required=True, type=Path)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    upstream, libnaomi, source = args.upstream.resolve(), args.libnaomi.resolve(), args.source.resolve()
    checked_revision(upstream, UPSTREAM_COMMIT, "SM64 upstream")
    checked_revision(libnaomi, LIBNAOMI_COMMIT, "libnaomi")

    controller_dir = upstream / "src/pc/controller"
    shutil.copy2(source / "port/controller_naomi.c", controller_dir / "controller_naomi.c")
    shutil.copy2(source / "port/controller_naomi.h", controller_dir / "controller_naomi.h")
    shutil.copy2(source / "port/naomi_maple_kos_compat.h", controller_dir / "naomi_maple_kos_compat.h")
    shutil.copy2(source / "port/sm64_naomi_oscont.h", controller_dir / "sm64_naomi_oscont.h")
    shutil.copy2(source / "port/sm64_naomi_jvs.h", controller_dir / "sm64_naomi_jvs.h")
    jvs = controller_dir / "sm64_naomi_jvs.h"
    text = jvs.read_text()
    text = replace_once(text, "#include <naomi/maple.h>", '#include "maple_naomi.h"', "Naomi JVS header")
    jvs.write_text(text)
    oscont = controller_dir / "sm64_naomi_oscont.h"
    text = oscont.read_text()
    text = replace_once(text, "#include <naomi/maple.h>", '#include "maple_naomi.h"', "Naomi OSCont header")
    oscont.write_text(text)

    maple_header = (libnaomi / "libnaomi/naomi/maple.h").read_text()
    (controller_dir / "maple_naomi.h").write_text(maple_header)
    maple_source = (libnaomi / "libnaomi/maple.c").read_text()
    maple_source = replace_once(
        maple_source,
        """#include "naomi/maple.h"
#include "naomi/system.h"
#include "naomi/thread.h"
#include "naomi/interrupt.h"
#include "irqinternal.h""",
        """#include "maple_naomi.h"
#include "naomi_maple_kos_compat.h""",
        "Maple platform headers",
    )
    maple_source = replace_all(maple_source, "mutex_try_lock", "sm64_naomi_mutex_try_lock", "KOS try-lock semantics")
    maple_source = replace_all(maple_source, "mutex_free", "mutex_destroy", "KOS mutex destroy API")
    maple_source = replace_once(maple_source, "mutex_init(&maple_mutex);", "mutex_init(&maple_mutex, MUTEX_TYPE_NORMAL);", "KOS mutex initialization")
    maple_source = "#if defined(__NAOMI__) && defined(TARGET_NAOMI)\n" + maple_source + "\n#endif\n"
    (controller_dir / "maple_naomi_kos.c").write_text(maple_source)

    controller = controller_dir / "controller_naomi.c"
    text = controller.read_text()
    text = replace_once(text, "#include <naomi/maple.h>", '#include "maple_naomi.h"', "local JVS header")
    text = replace_once(text, "    /* The Naomi platform startup owns Maple initialization. */", "    /* KOS needs explicit Maple/JVS initialization. */\n    _maple_init();", "KOS Maple initialization")
    text = text.replace('#include "sm64_naomi_oscont.h"', '#include "sm64_naomi_oscont.h"\nextern void _maple_init(void);')
    controller.write_text(text)

    entry = controller_dir / "controller_entry_point.c"
    text = entry.read_text()
    text = replace_once(text, """#if !defined(TARGET_PSP) && !defined(TARGET_DC)
#include "controller_keyboard.h"
#endif""", """#if !defined(TARGET_PSP) && !defined(TARGET_DC) && !defined(TARGET_NAOMI)
#include "controller_keyboard.h"
#endif""", "keyboard include guard")
    text = replace_once(text, """#elif defined(TARGET_DC)
#include "controller_dc.h"
#else""", """#elif defined(TARGET_DC)
#include "controller_dc.h"
#elif defined(TARGET_NAOMI)
#include "controller_naomi.h"
#else""", "Naomi controller include")
    text = replace_once(text, """#if !defined(TARGET_PSP) && !defined(TARGET_DC)
    &controller_recorded_tas,
    &controller_keyboard,
#endif""", """#if !defined(TARGET_PSP) && !defined(TARGET_DC) && !defined(TARGET_NAOMI)
    &controller_recorded_tas,
    &controller_keyboard,
#endif""", "keyboard registry guard")
    text = replace_once(text, """#elif defined(TARGET_DC)
    &controller_dc,
#else""", """#elif defined(TARGET_DC)
    &controller_dc,
#elif defined(TARGET_NAOMI)
    &controller_naomi,
#else""", "Naomi controller registration")
    entry.write_text(text)

    makefile = upstream / "Makefile"
    text = makefile.read_text()
    text = replace_once(text, "PLATFORM_CFLAGS  := $(KOS_CFLAGS) -DTARGET_DC -DNDEBUG -Wall -Wextra -g3", "PLATFORM_CFLAGS  := $(KOS_CFLAGS) -DTARGET_DC -DTARGET_NAOMI -DNDEBUG -Wall -Wextra -g3", "Naomi KOS target flags")
    makefile.write_text(text)
    print(f"Applied Naomi/KOS overlay to SM64 {UPSTREAM_COMMIT}")


if __name__ == "__main__":
    main()
