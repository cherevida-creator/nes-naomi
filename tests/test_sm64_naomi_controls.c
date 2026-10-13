#include <assert.h>
#include "sm64_naomi_jvs.h"

int main(void)
{
    jvs_buttons_t jvs = { 0 };
    sm64_n64_input_t out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.stick_x == 0 && out.stick_y == 0 && out.buttons == 0);

    jvs.player1.right = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.stick_x == 80 && out.stick_y == 0);

    jvs.player1.up = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.stick_x == 57 && out.stick_y == 57);

    jvs.player1.left = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.stick_x == 0 && out.stick_y == 80);

    jvs = (jvs_buttons_t){ 0 };
    jvs.player1.button1 = jvs.player1.button2 = jvs.player1.button3 = 1;
    jvs.player1.button4 = jvs.player1.button5 = jvs.player1.button6 = 1;
    jvs.player1.start = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.buttons == (SM64_N64_A | SM64_N64_B | SM64_N64_Z |
                           SM64_N64_CLEFT | SM64_N64_CRIGHT |
                           SM64_N64_R | SM64_N64_START));

    /* Player 2 input must not leak into this Player 1 adapter. */
    jvs = (jvs_buttons_t){ 0 };
    jvs.player2.button1 = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.buttons == 0);
    return 0;
}
#include <assert.h>
#include "sm64_naomi_jvs.h"

int main(void)
{
    jvs_buttons_t jvs = { 0 };
    sm64_n64_input_t out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.stick_x == 0 && out.stick_y == 0 && out.buttons == 0);

    jvs.player1.right = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.stick_x == 80 && out.stick_y == 0);

    jvs.player1.up = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.stick_x == 57 && out.stick_y == 57);

    jvs.player1.left = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.stick_x == 0 && out.stick_y == 57);

    jvs = (jvs_buttons_t){ 0 };
    jvs.player1.button1 = jvs.player1.button2 = jvs.player1.button3 = 1;
    jvs.player1.button4 = jvs.player1.button5 = jvs.player1.button6 = 1;
    jvs.player1.start = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.buttons == (SM64_N64_A | SM64_N64_B | SM64_N64_Z |
                           SM64_N64_CLEFT | SM64_N64_CRIGHT |
                           SM64_N64_R | SM64_N64_START));

    /* Player 2 input must not leak into this Player 1 adapter. */
    jvs = (jvs_buttons_t){ 0 };
    jvs.player2.button1 = 1;
    out = sm64_naomi_map_jvs_p1(jvs);
    assert(out.buttons == 0);
    return 0;
}
