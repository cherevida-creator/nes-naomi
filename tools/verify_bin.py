#!/usr/bin/env python3
import os, sys
p=sys.argv[1]
s=os.path.getsize(p)
if s < 0x10000:
    raise SystemExit(f"ERROR: {p} is suspiciously small ({s} bytes)")
with open(p,'rb') as f: h=f.read(0x100)
# Naomi ROM headers are text-rich; keep validation conservative and non-destructive.
if b"NES Naomi" not in h:
    print("WARNING: title not found in first 256 bytes; inspect makerom output/header.")
print(f"OK: {p} exists, {s} bytes")
