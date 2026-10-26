#include <naomi/maple.h>
#include <naomi/video.h>

#include "sm64_naomi_jvs.h"

static void draw_input_test(void)
{
    const color_t white = rgb(255, 255, 255);
    const color_t green = rgb(96, 255, 96);
    const color_t red = rgb(255, 96, 96);
    jvs_buttons_t jvs = { 0 };
    const int sample_valid = maple_poll_buttons() == 0;

    if (sample_valid) {
        jvs = maple_buttons_held();
    }

    const sm64_n64_input_t input = sm64_naomi_map_jvs_p1(jvs);
    const color_t status = sample_valid ? green : red;

    video_set_background_color(rgb(8, 16, 40));
    video_draw_debug_text(24, 24, white, "SUPER MARIO 64 - NAOMI 2 INPUT TEST");
    video_draw_debug_text(24, 48, status, "JVS PLAYER 1: %s",
                          sample_valid ? "CONNECTED" : "NO SAMPLE");
    video_draw_debug_text(24, 80, white, "N64 STICK X: %d  Y: %d",
                          input.stick_x, input.stick_y);
    video_draw_debug_text(24, 112, white, "N64 BUTTON MASK: %04X", input.buttons);
    video_draw_debug_text(24, 152, white,
                          "ARCADE BUTTONS 1-6 -> A B Z C-LEFT C-RIGHT R");
    video_draw_debug_text(24, 176, white, "PLAYER 1 START -> START");
    video_draw_debug_text(24, 208, white, "MOVE THE JOYSTICK AND PRESS EACH BUTTON");
    video_display_on_vblank();
}

void main(void)
{
    video_init(VIDEO_COLOR_1555);
    while (1) {
        draw_input_test();
    }
}

void test(void)
{
    main();
}
