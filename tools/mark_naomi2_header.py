#!/usr/bin/env python3
"""Mark a libnaomi-made image as Naomi 2 without changing its payload."""

import argparse
from pathlib import Path

NAOMI_1 = b"NAOMI           "
NAOMI_2 = b"Naomi2          "
HEADER_LENGTH = 0x500


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bin", type=Path)
    args = parser.parse_args()

    data = args.bin.read_bytes()
    if len(data) <= HEADER_LENGTH:
        raise SystemExit(f"BIN is too small to contain a Naomi ROM: {len(data)} bytes")
    if data[HEADER_LENGTH - 1] != 0xFF:
        raise SystemExit("invalid Naomi header terminator")

    version = data[:len(NAOMI_2)]
    if version == NAOMI_1:
        data = NAOMI_2 + data[len(NAOMI_1):]
    elif version != NAOMI_2:
        raise SystemExit(f"unsupported Naomi ROM header: {version!r}")

    if data[:len(NAOMI_2)] != NAOMI_2 or data[HEADER_LENGTH - 1] != 0xFF:
        raise SystemExit("failed to verify Naomi 2 header")

    args.bin.write_bytes(data)
    print(f"Marked Naomi 2 header: {args.bin} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
