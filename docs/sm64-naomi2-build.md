# SM64 Naomi 2 integration status

The repository is still the NES emulator project; it does not yet build a playable Super Mario 64 game. The integration now contains a Player 1 controller overlay for Dreamcast-Projects/sm64-port-lat, pinned at commit e4574b577609a51c6b7ca7914d2f25436831eede.

## Integrated and checked

- JVS Player 1 joystick directions map to the N64 analog stick, with normalized diagonals and opposite directions cancelling.
- Buttons 1–6 map to A, B, Z, C-left, C-right and R. Player 1 Start maps to Start.
- The controller polls libnaomi once for each SM64 controller read and clears stale input when polling fails.
- tools/integrate_sm64_naomi.py applies a guarded, pinned overlay to the upstream ControllerAPI registry. GitHub Actions verifies the patch point and compiles the controller for host and SH-4.
- The existing mapping assertions run on the host.

## Still needed for a NetDimm BIN

The integration does not provide Naomi 2 startup or Maple initialization, video rendering, audio output, a Naomi-target build system, or NetDimm packaging. The upstream Dreamcast TARGET_DC build is not a Naomi image. The current Actions workflow checks the controller object and mapping only; it does not build the full game or produce a BIN.

The original SM64 engine, graphics and audio have not been rewritten or replaced. No commercial ROM is stored in the public repository; any asset extraction must use the user's base ROM locally. A BIN will only be called functional after the complete Naomi image is built and verified in an emulator or on Naomi 2 hardware.

Upstream source: Dreamcast-Projects/sm64-port-lat at e4574b577609a51c6b7ca7914d2f25436831eede.
