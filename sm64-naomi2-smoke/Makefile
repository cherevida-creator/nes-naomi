# Builds a standalone Naomi diagnostic BIN using DragonMinded/libnaomi.
# Set LIBNAOMI_SRC to the checked-out libnaomi source tree.

all: sm64_naomi2_smoke.bin

SRCS += main.c
FLAGS += -I../port
LIBNAOMI_SRC ?= ../libnaomi
include $(LIBNAOMI_SRC)/Makefile.base

sm64_naomi2_smoke.bin: $(MAKEROM_FILE) $(NAOMI_BIN_FILE)
	$(MAKEROM) $@ \
		--title "SM64 Naomi Input Test" \
		--publisher "Naomi Port Test" \
		--serial "B64T" \
		--section $(NAOMI_BIN_FILE),$(START_ADDR) \
		--entrypoint $(MAIN_ADDR) \
		--main-binary-includes-test-binary \
		--test-entrypoint $(TEST_ADDR)
	$(VENV_PYTHON3) ../tools/mark_naomi2_header.py $@

.PHONY: clean
clean:
	rm -rf build sm64_naomi2_smoke.bin
