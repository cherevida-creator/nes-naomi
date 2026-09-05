# NES Naomi - 31 kHz / NetDIMM build
# Pinned core: PeakRacing/nes 69e433da8bd1eaf993659991f30b4989b77dad2c

all: nes_naomi.bin

ENABLE_WALL := 0
OPTIMIZATION_LEVEL := -O2
SERIAL := BNES
FLAGS += -Ivendor/nes-core/inc -Iport

SRCS += main.c
SRCS += menu/rom_menu.c
SRCS += port/nes_port_naomi.c
SRCS += vendor/nes-core/src/nes.c
SRCS += vendor/nes-core/src/nes_apu.c
SRCS += vendor/nes-core/src/nes_cpu.c
SRCS += vendor/nes-core/src/nes_default.c
SRCS += vendor/nes-core/src/nes_mapper.c
SRCS += vendor/nes-core/src/nes_ppu.c
SRCS += vendor/nes-core/src/nes_rom.c
SRCS += $(wildcard vendor/nes-core/src/nes_mapper/*.c)

include ${NAOMI_BASE}/Makefile.base

build/romfs.bin: roms/ ${ROMFSGEN_FILE}
	@rm -rf build/romfs-tree
	@mkdir -p build/romfs-tree/roms
	@cp -a roms/. build/romfs-tree/roms/
	${ROMFSGEN} $@ build/romfs-tree/

nes_naomi.bin: ${MAKEROM_FILE} ${NAOMI_BIN_FILE} build/romfs.bin
	${MAKEROM} $@ \
		--title "NES Naomi" \
		--publisher "Homebrew" \
		--serial "${SERIAL}" \
		--section ${NAOMI_BIN_FILE},${START_ADDR} \
		--entrypoint ${MAIN_ADDR} \
		--main-binary-includes-test-binary \
		--test-entrypoint ${TEST_ADDR} \
		--align-before-data 4 \
		--filedata build/romfs.bin

.PHONY: clean
clean:
	rm -rf build nes_naomi.bin
