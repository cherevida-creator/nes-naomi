#ifndef SM64_NAOMI_OSCONT_H
#define SM64_NAOMI_OSCONT_H

#include <PR/os_cont.h>
#include <naomi/maple.h>

#include "sm64_naomi_jvs.h"

/* Fill the upstream SM64 controller pad from one JVS Player 1 sample. */
static inline void sm64_naomi_fill_oscont(OSContPad *pad, jvs_buttons_t jvs,
                                         int sample_valid)
{
    sm64_n64_input_t input;

    pad->button = 0;
    pad->stick_x = 0;
    pad->stick_y = 0;
    pad->errnum = sample_valid ? 0 : CONT_NO_RESPONSE_ERROR;
    if (!sample_valid) return;

    input = sm64_naomi_map_jvs_p1(jvs);
    pad->stick_x = input.stick_x;
    pad->stick_y = input.stick_y;
    pad->button = input.buttons;
}

#endif
