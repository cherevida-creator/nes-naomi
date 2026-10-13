#ifndef SM64_NAOMI_JVS_H
#define SM64_NAOMI_JVS_H

#include <naomi/maple.h>
#include "sm64_naomi_controls.h"

/*
 * Convert libnaomi's current JVS sample for Player 1. Call this with the
 * result of maple_buttons_held() after maple_poll_buttons() succeeds.
 */
static inline sm64_n64_input_t sm64_naomi_map_jvs_p1(jvs_buttons_t jvs)
{
    const player_buttons_t p = jvs.player1;
    const sm64_naomi_p1_t in = {
        .left = p.left,
        .right = p.right,
        .up = p.up,
        .down = p.down,
        .button1 = p.button1,
        .button2 = p.button2,
        .button3 = p.button3,
        .button4 = p.button4,
        .button5 = p.button5,
        .button6 = p.button6,
        .start = p.start,
    };
    return sm64_naomi_map_p1(in);
}

#endif
