# Super Mario 64 Naomi 2 build

The Naomi 2 port is built from the pinned Dreamcast-Projects/sm64-port-lat
revision and a local US baserom. The baserom is read from SM64_BASEROM; it is
not copied into this repository.

## Build

Requirements: KallistiOS with the SH-4 toolchain, CMake, Git, Python 3, and a
legally obtained baserom.us.z64.

    source /path/to/kos/environ.sh
    export SM64_BASEROM=/path/to/baserom.us.z64
    bash tools/build_sm64_naomi2.sh

The build fetches GLdc at commit
f06c72ff145d5354467739f26264160a996e3a2d, applies the Naomi JVS controller
overlay, and produces mario64-naomi2.bin. Player 1 joystick directions map to
the N64 stick; arcade buttons 1–6 map to A, B, Z, C-left, C-right, and R;
Player 1 Start maps to Start.

The packer takes the image's SH-4 load address and entry point from its ELF.
It also applies a guarded one-character fix to KOS naomibintool's -b
file:address parser, which otherwise parses the load address as zero. Before
returning successfully, the build checks that the Naomi header contains the
same load address and entry point as the ELF.

## Verification status

A successful cross-build and matching Naomi header verify the SH-4 image and
container metadata. They do not verify game execution, video, audio, or JVS
input on Naomi 2. Confirm those in Flycast or on hardware before treating a
generated BIN as a working release.
