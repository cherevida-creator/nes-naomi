#!/usr/bin/env python3
"""Apply the Naomi controller overlay to the pinned SM64 Dreamcast tree."""
import argparse
import shutil
import subprocess
from pathlib import Path

UPSTREAM_COMMIT = "e4574b577609a51c6b7ca7914d2f25436831eede"


def replace_once(source: str, before: str, after: str, label: str) -> str:
    count = source.count(before)
    if count != 1:
        raise SystemExit(f"expected one {label} insertion point, found {count}")
    return source.replace(before, after, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", required=True, type=Path)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    upstream = args.upstream.resolve()
    source = args.source.resolve()

    actual = subprocess.check_output(
        ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != UPSTREAM_COMMIT:
        raise SystemExit(f"upstream revision mismatch: expected {UPSTREAM_COMMIT}, got {actual}")

    controller_dir = upstream / "src/pc/controller"
    shutil.copy2(source / "port/controller_naomi.c", controller_dir / "controller_naomi.c")
    shutil.copy2(source / "port/controller_naomi.h", controller_dir / "controller_naomi.h")

    entry = controller_dir / "controller_entry_point.c"
    text = entry.read_text()
    text = replace_once(
        text,
        '#if !defined(TARGET_PSP) && !defined(TARGET_DC)\n#include "controller_keyboard.h"\n#endif',
        '#if !defined(TARGET_PSP) && !defined(TARGET_DC) && !defined(TARGET_NAOMI)\n#include "controller_keyboard.h"\n#endif',
        "keyboard include guard",
    )
    text = replace_once(
        text,
        '#elif defined(TARGET_DC)\n#include "controller_dc.h"\n#else',
        '#elif defined(TARGET_DC)\n#include "controller_dc.h"\n#elif defined(TARGET_NAOMI)\n#include "controller_naomi.h"\n#else',
        "Naomi controller include",
    )
    text = replace_once(
        text,
        '#if !defined(TARGET_PSP) && !defined(TARGET_DC)\n    &controller_recorded_tas,\n    &controller_keyboard,\n#endif',
        '#if !defined(TARGET_PSP) && !defined(TARGET_DC) && !defined(TARGET_NAOMI)\n    &controller_recorded_tas,\n    &controller_keyboard,\n#endif',
        "keyboard registry guard",
    )
    text = replace_once(
        text,
        '#elif defined(TARGET_DC)\n    &controller_dc,\n#else',
        '#elif defined(TARGET_DC)\n    &controller_dc,\n#elif defined(TARGET_NAOMI)\n    &controller_naomi,\n#else',
        "Naomi controller registration",
    )
    entry.write_text(text)
    print(f"Applied Naomi Player 1 controller overlay to {actual}")


if __name__ == "__main__":
    main()
