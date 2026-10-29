#!/usr/bin/env python3
"""Check Naomi 2 marking is safe and idempotent."""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "tools/mark_naomi2_header.py"
PAYLOAD = b"SH4 executable bytes"


def run(path: Path) -> None:
    subprocess.run([sys.executable, str(SCRIPT), str(path)], check=True)


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "test.bin"
        original = bytearray(b"NAOMI           " + b"\0" * (0x500 - 17) + b"\xFF")
        original.extend(PAYLOAD)
        path.write_bytes(original)

        run(path)
        first = path.read_bytes()
        run(path)
        second = path.read_bytes()

        assert first[:16] == b"Naomi2          "
        assert first[16:0x500] == original[16:0x500]
        assert first[0x500:] == PAYLOAD
        assert second == first


if __name__ == "__main__":
    main()
