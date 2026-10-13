#include "controller_naomi.h"
#include <naomi/maple.h>

#include "sm64_naomi_oscont.h"

static void controller_naomi_init(void)
{
    /* The Naomi platform startup owns Maple initialization. */
}

static void controller_naomi_read(OSContPad *pad)
{
    const int sample_valid = maple_poll_buttons() == 0;
    jvs_buttons_t jvs = { 0 };

    if (sample_valid) jvs = maple_buttons_held();
    sm64_naomi_fill_oscont(pad, jvs, sample_valid);
}

struct ControllerAPI controller_naomi = {
    controller_naomi_init,
    controller_naomi_read,
};
