#ifndef ROM_MENU_H
#define ROM_MENU_H

#include <stddef.h>

#define ROM_MENU_MAX_ROMS 256
#define ROM_MENU_NAME_MAX 128

typedef struct {
    char name[ROM_MENU_NAME_MAX];
    char path[ROM_MENU_NAME_MAX + 32];
} rom_entry_t;

typedef struct {
    rom_entry_t entries[ROM_MENU_MAX_ROMS];
    int count;
    int selected;
    int top;
} rom_menu_t;

int rom_menu_scan(rom_menu_t *menu);
void rom_menu_move(rom_menu_t *menu, int delta);
const rom_entry_t *rom_menu_selected(const rom_menu_t *menu);
void rom_menu_draw(const rom_menu_t *menu);

#endif
