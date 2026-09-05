#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <naomi/video.h>
#include <naomi/audio.h>
#include <naomi/maple.h>
#include "nes.h"

#define OUT_W 640
#define OUT_H 480
#define NES_X_OFFSET 64

static int audio_ready = 0;

void *nes_malloc(int num) { return malloc((size_t)num); }
void nes_free(void *address) { free(address); }
void *nes_memcpy(void *d, const void *s, size_t n) { return memcpy(d, s, n); }
void *nes_memset(void *d, int c, size_t n) { return memset(d, c, n); }
int nes_memcmp(const void *a, const void *b, size_t n) { return memcmp(a, b, n); }

#if (NES_USE_FS == 1)
FILE *nes_fopen(const char *filename, const char *mode) { return fopen(filename, mode); }
size_t nes_fread(void *ptr, size_t size, size_t nmemb, FILE *stream) { return fread(ptr, size, nmemb, stream); }
size_t nes_fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream) { return fwrite(ptr, size, nmemb, stream); }
int nes_fseek(FILE *stream, long int offset, int whence) { return fseek(stream, offset, whence); }
int nes_fclose(FILE *stream) { return fclose(stream); }
#endif

#if (NES_ENABLE_SOUND == 1)
int nes_sound_output(uint8_t *buffer, size_t len)
{
    if (!audio_ready || buffer == NULL || len == 0) return 0;
    static uint8_t stereo[NES_APU_SAMPLE_PER_SYNC * 2 + 16];
    if (len > NES_APU_SAMPLE_PER_SYNC) len = NES_APU_SAMPLE_PER_SYNC;
    for (size_t i = 0; i < len; i++) {
        stereo[i * 2] = buffer[i];
        stereo[i * 2 + 1] = buffer[i];
    }
    audio_write_stereo_data(stereo, (unsigned int)len);
    return 0;
}
#endif

int nes_initex(nes_t *nes)
{
    (void)nes;
#if (NES_ENABLE_SOUND == 1)
    if (!audio_ready) {
        audio_init();
        if (audio_register_ringbuffer(AUDIO_FORMAT_8BIT, NES_APU_SAMPLE_RATE, 4096) == 0) {
            audio_ready = 1;
            audio_change_ringbuffer_volume(1.0f);
        }
    }
#endif
    return 0;
}

int nes_deinitex(nes_t *nes)
{
    (void)nes;
#if (NES_ENABLE_SOUND == 1)
    if (audio_ready) {
        audio_unregister_ringbuffer();
        audio_free();
        audio_ready = 0;
    }
#endif
    return 0;
}

static inline uint16_t rgb565_to_naomi1555(uint16_t s)
{
    uint16_t r = (uint16_t)((s >> 11) & 0x1F);
    uint16_t g = (uint16_t)(((s >> 5) & 0x3F) >> 1);
    uint16_t b = (uint16_t)(s & 0x1F);
    return (uint16_t)(0x8000u | (r << 10) | (g << 5) | b);
}

int nes_draw(int x1, int y1, int x2, int y2, nes_color_t *color_data)
{
    if (!color_data) return -1;
    if (x1 < 0 || y1 < 0 || x2 >= NES_WIDTH || y2 >= NES_HEIGHT || x2 < x1 || y2 < y1) return -1;

    uint16_t *fb = (uint16_t *)video_framebuffer();
    if (!fb) return -1;
    const int src_w = x2 - x1 + 1;

    for (int y = y1; y <= y2; y++) {
        int sy = y - y1;
        uint16_t *row0 = fb + (y * 2) * OUT_W + NES_X_OFFSET + x1 * 2;
        uint16_t *row1 = row0 + OUT_W;
        for (int x = x1; x <= x2; x++) {
            uint16_t p = rgb565_to_naomi1555(color_data[sy * src_w + (x - x1)]);
            int dx = (x - x1) * 2;
            row0[dx] = p;
            row0[dx + 1] = p;
            row1[dx] = p;
            row1[dx + 1] = p;
        }
    }
    return 0;
}

void nes_frame(nes_t *nes)
{
    if (maple_poll_buttons() == 0) {
        jvs_buttons_t held = maple_buttons_held();
        jvs_buttons_t pressed = maple_buttons_pressed();

        nes->nes_cpu.joypad.U1 = held.player1.up ? 1 : 0;
        nes->nes_cpu.joypad.D1 = held.player1.down ? 1 : 0;
        nes->nes_cpu.joypad.L1 = held.player1.left ? 1 : 0;
        nes->nes_cpu.joypad.R1 = held.player1.right ? 1 : 0;
        nes->nes_cpu.joypad.B1 = held.player1.button1 ? 1 : 0;
        nes->nes_cpu.joypad.A1 = held.player1.button2 ? 1 : 0;
        nes->nes_cpu.joypad.ST1 = held.player1.start ? 1 : 0;
        nes->nes_cpu.joypad.SE1 = held.player1.service ? 1 : 0;

        if (pressed.player1.button3) nes->nes_quit = 1;
    }
    video_display_on_vblank();
}
