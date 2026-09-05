#include <stdio.h>
#include <string.h>
#include <naomi/video.h>
#include <naomi/romfs.h>
#include <naomi/maple.h>
#include "nes.h"
#include "menu/rom_menu.h"

static void play_rom(const char *path)
{
    nes_t *nes = nes_init();
    if (!nes) return;

    video_fill_screen(rgb(0,0,0));
    video_display_on_vblank();

    if (nes_load_file(nes, path) == NES_OK) {
        nes_run(nes);
        nes_unload_file(nes);
    }
    nes_deinit(nes);

    video_fill_screen(rgb(0,0,0));
    video_display_on_vblank();
}

void main(void)
{
    video_init(VIDEO_COLOR_1555); /* libnaomi current: 640x480@60 VGA / 31 kHz */
    video_set_background_color(rgb(0, 0, 0));
    romfs_init_default();

    rom_menu_t menu;
    rom_menu_scan(&menu);

    while (1) {
        if (maple_poll_buttons() == 0) {
            jvs_buttons_t p = maple_buttons_pressed();
            if (p.player1.up) rom_menu_move(&menu, -1);
            if (p.player1.down) rom_menu_move(&menu, 1);
            if (p.player1.button1) {
                const rom_entry_t *entry = rom_menu_selected(&menu);
                if (entry) play_rom(entry->path);
            }
        }
        rom_menu_draw(&menu);
        video_display_on_vblank();
    }
}

void test(void)
{
    main();
}
