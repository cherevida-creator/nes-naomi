#ifndef SM64_NAOMI_CONTROLS_H
#define SM64_NAOMI_CONTROLS_H

#include <stdint.h>

/* One JVS Player 1 sample, independent of KOS/libnaomi headers. */
typedef struct {
    uint8_t left, right, up, down;
    uint8_t button1, button2, button3, button4, button5, button6;
    uint8_t start;
} sm64_naomi_p1_t;

typedef struct {
    int8_t stick_x;
    int8_t stick_y;
    uint16_t buttons;
} sm64_n64_input_t;

enum {
    SM64_N64_A      = 0x8000,
    SM64_N64_B      = 0x4000,
    SM64_N64_Z      = 0x2000,
    SM64_N64_START  = 0x1000,
    SM64_N64_R      = 0x0010,
    SM64_N64_CLEFT  = 0x0002,
    SM64_N64_CRIGHT = 0x0001
};

/*
 * JVS joystick -> N64 analog stick. Diagonals are normalized to 57/80;
 * contradictory directions cancel. B1=A (jump), B2=B (action), B3=Z,
 * B4=C-left, B5=C-right, B6=R, and Player 1 Start=Start.
 */
static inline sm64_n64_input_t sm64_naomi_map_p1(sm64_naomi_p1_t in)
{
    sm64_n64_input_t out = { 0, 0, 0 };
    const int x = (in.right != 0) - (in.left != 0);
    const int y = (in.up != 0) - (in.down != 0);
    const int magnitude = (x != 0 && y != 0) ? 57 : 80;

    out.stick_x = (int8_t)(x * magnitude);
    out.stick_y = (int8_t)(y * magnitude);
    if (in.button1) out.buttons |= SM64_N64_A;
    if (in.button2) out.buttons |= SM64_N64_B;
    if (in.button3) out.buttons |= SM64_N64_Z;
    if (in.button4) out.buttons |= SM64_N64_CLEFT;
    if (in.button5) out.buttons |= SM64_N64_CRIGHT;
    if (in.button6) out.buttons |= SM64_N64_R;
    if (in.start)   out.buttons |= SM64_N64_START;
    return out;
}

#endif
