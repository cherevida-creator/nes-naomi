# SM64 Naomi 2 build status

This repository does not yet contain a playable Super Mario 64 port. The upstream Dreamcast-Projects/sm64-port-lat tree is Dreamcast-oriented; its TARGET_DC=1 output is not a Naomi NetDimm image.

This CI milestone verifies only the shared input adapter:

- JVS Player 1 joystick directions map to the N64 analog stick.
- Diagonals are normalized to avoid faster diagonal movement; opposite directions cancel.
- Buttons 1–6 map to A, B, Z, C-left, C-right and R; Player 1 Start maps to Start.
- GitHub Actions runs host assertions and cross-compiles the adapter with an SH-4 toolchain from a KallistiOS development image.

The workflow does not package or upload a game BIN. A real NetDimm image still needs a Naomi 2 video/audio backend, JVS input polling integration, Naomi startup/link configuration, and a NetDimm image packager. Those pieces must be built and verified before calling an artifact playable. No ROM is stored or published; asset extraction uses the user's base ROM kept outside the public repository.

Upstream source reference: Dreamcast-Projects/sm64-port-lat, inspected at commit e4574b577609a51c6b7ca7914d2f25436831eede.
