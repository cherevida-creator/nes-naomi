# SM64 Naomi 1 compatibility — 2026-11-14

Experimental milestone; not a finished port.

## Preserved original
The Oct 30 candidate was recovered on IvanPC, 12450608 bytes,
SHA256 efe77249d1fdb5f96e8cdaba8c20910b6a8db84ed09b86ea48a44a04d2f07378.
Original working tree, vendor sources/builds, original ELF, SH4 toolchain,
container root filesystem and private baserom were backed up separately
before modifying a copy. Private backups remain on IvanPC, not GitHub.

## Native build
Based on 8a88b2913dc61eca571a3aae4f462d8bb865169a.
Recovered local fixes retain GLdc and the original SM64 engine.
KOS revision d81aa3fda0520b6ca64098ce9d1d43e7562142d9.
Run tools/build_sm64_naomi1.sh inside the recovered build container,
mounting this tree as /src, the SH4 toolchain at /opt/toolchains/dc/sh-elf
and the user's ROM directory read-only as /rom.
The wrapper uses /rom/Super Mario 64 (USA).z64.
tools/build_sm64_naomi2.sh defaults to the existing Naomi2 output;
SM64_PLATFORM_SIGNATURE=NAOMI and SM64_OUTPUT_BIN select the experimental output.
Link map: vendor/sm64-port-lat/build/us_dc/sm64.naomi.map.
No ROM, extracted assets or game binaries are published here.

## Candidate
SM64_NAOMI1_COMPAT_EXPERIMENTAL.bin: 12450608 bytes.
SHA256 97a3684872e0765b9e460d333b3f0fe3d2c4448c60c06ec7eb0f0f757ad2b0f1.
Header signature NAOMI; load and entry 0x8c020000.
Payload after byte 4096 was compared byte-for-byte with the preserved
original and is identical. Full rebuild also reproduced that payload.

## Tests
Unmodified official Flycast 2.7, isolated copies/configurations.
Original Naomi2-header BIN under an unknown basename reproduces BIOS rejection.
Experimental NAOMI BIN uses its own filename and boots Naomi 1.
The identical experimental BIN also boots when Flycast selects Naomi 2.
For that platform-selection diagnostic only, a separate copy was named wldrider.bin.
This alias is not the release identity or an independent filename-based Naomi2
launcher. A proper own-name Naomi2 selection method remains pending.
Title, file menu, loaded pre-existing save, 3D castle grounds, movement and jump observed.
Screenshots and per-case logs are stored in the private recovery folder.
Windows loopback capture during the Naomi1 test contains nonzero PCM.
This is not proof of original-equivalent audio or complete sound-effect coverage.
Displayed FPS observations around 26–31; not a reliable sustained benchmark.

## Memory
ELF static sections: text 9675988, data 2763140, BSS 2838372 bytes.
Highest loaded segment end: 0x8ceb3aa4, within Naomi1 main RAM.
No ELAN/PVR2 symbols found in the generated link map.
KOS PVR allocator limits select 16 MiB on Naomi; SPU selects 8 MiB.
Dynamic high-water RAM, VRAM and ARAM usage has not been measured.
No physical Naomi/NetDimm test has been performed.

## Known blockers
Upstream TARGET_DC EEPROM read deliberately loads a baked-in 120-star save.
TARGET_DC EEPROM write returns success without persistence.
The 120/119-star menu is not evidence of completing the game.
Save persistence must be implemented for actual Naomi storage and power-cycle tested.
Full new-game introduction, castle entry, Bob-omb Battlefield and first star
have not been verified in this phase.
Black sky backgrounds are visible outdoors; graphical fidelity is incomplete.
All six JVS buttons and analog-speed compromise need end-to-end validation.
No migration to the alternative raw PowerVR backend was performed.
