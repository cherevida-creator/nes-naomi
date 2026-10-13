#include <assert.h>
#include "sm64_naomi_controls.h"

int main(void)
{
    sm64_naomi_p1_t in = { 0 };
    sm64_n64_input_t out = sm64_naomi_map_p1(in);
    assert(out.stick_x == 0 && out.stick_y == 0 && out.buttons == 0);

    in.right = 1;
    out = sm64_naomi_map_p1(in);
    assert(out.stick_x == 80 && out.stick_y == 0);

    in.up = 1;
    out = sm64_naomi_map_p1(in);
    assert(out.stick_x == 57 && out.stick_y == 57);

    in.left = 1;
    out = sm64_naomi_map_p1(in);
    assert(out.stick_x == 0 && out.stick_y == 80);

    in = (sm64_naomi_p1_t){ 0 };
    in.button1 = in.button2 = in.button3 = 1;
    in.button4 = in.button5 = in.button6 = in.start = 1;
    out = sm64_naomi_map_p1(in);
    assert(out.buttons == (SM64_N64_A | SM64_N64_B | SM64_N64_Z |
                           SM64_N64_CLEFT | SM64_N64_CRIGHT |
                           SM64_N64_R | SM64_N64_START));
    return 0;
}
