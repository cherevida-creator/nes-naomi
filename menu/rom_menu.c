#include "rom_menu.h"
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <naomi/video.h>

static int has_nes_extension(const char *name)
{
    size_t n = strlen(name);
    return n >= 4 && strcasecmp(name + n - 4, ".nes") == 0;
}

static int entry_cmp(const void *a, const void *b)
{
    const rom_entry_t *ea = (const rom_entry_t *)a;
    const rom_entry_t *eb = (const rom_entry_t *)b;
    return strcasecmp(ea->name, eb->name);
}

int rom_menu_scan(rom_menu_t *menu)
{
    memset(menu, 0, sizeof(*menu));
    DIR *dir = opendir("rom://roms");
    if (!dir) return -1;

    struct dirent *ent;
    while ((ent = readdir(dir)) != NULL && menu->count < ROM_MENU_MAX_ROMS)
    {
        if (!has_nes_extension(ent->d_name)) continue;
        rom_entry_t *dst = &menu->entries[menu->count++];
        snprintf(dst->name, sizeof(dst->name), "%s", ent->d_name);
        snprintf(dst->path, sizeof(dst->path), "rom://roms/%s", ent->d_name);
    }
    closedir(dir);

    if (menu->count > 1) qsort(menu->entries, (size_t)menu->count, sizeof(menu->entries[0]), entry_cmp);
    return menu->count;
}

void rom_menu_move(rom_menu_t *menu, int delta)
{
    if (menu->count <= 0) return;
    menu->selected += delta;
    while (menu->selected < 0) menu->selected += menu->count;
    while (menu->selected >= menu->count) menu->selected -= menu->count;
    if (menu->selected < menu->top) menu->top = menu->selected;
    if (menu->selected >= menu->top + 16) menu->top = menu->selected - 15;
}

const rom_entry_t *rom_menu_selected(const rom_menu_t *menu)
{
    if (!menu || menu->count <= 0) return NULL;
    return &menu->entries[menu->selected];
}

void rom_menu_draw(const rom_menu_t *menu)
{
    video_fill_screen(rgb(0, 0, 0));
    video_draw_debug_text(40, 28, rgb(255,255,255), "NES NAOMI - 31 kHz / 640x480p");
    video_draw_debug_text(40, 52, rgb(180,180,180), "Joystick: elegir   B1: jugar   B3: volver al menu");

    if (menu->count <= 0)
    {
        video_draw_debug_text(40, 110, rgb(255,220,80), "No hay archivos .nes en roms/");
        return;
    }

    int end = menu->top + 16;
    if (end > menu->count) end = menu->count;
    for (int i = menu->top; i < end; i++)
    {
        int y = 92 + ((i - menu->top) * 22);
        color_t c = (i == menu->selected) ? rgb(255,255,255) : rgb(150,150,150);
        video_draw_debug_text(52, y, c, "%c %s", (i == menu->selected) ? '>' : ' ', menu->entries[i].name);
    }
    video_draw_debug_text(40, 456, rgb(140,140,140), "%d ROM(s)", menu->count);
}
