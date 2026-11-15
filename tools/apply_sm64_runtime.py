#!/usr/bin/env python3
"""Opt-in SRAM save and exact 30 Hz pacing/telemetry; preserve graphics-only baseline."""
from pathlib import Path
import argparse
a=argparse.ArgumentParser();a.add_argument('--upstream',required=True);a.add_argument('--source',required=True);v=a.parse_args()
r=Path(v.upstream);root=Path(v.source)
p=r/'src/pc/ultra_reimplementation.c';s=p.read_text()
s=s.replace('#include "120_star_save.h"',(root/'port/sm64_naomi_sram.inc.c').read_text())
needle='s32 osEepromLongRead(UNUSED OSMesgQueue *mq, u8 address, u8 *buffer, int nbytes) {'
i=s.index(needle);j=s.index('s32 osEepromLongWrite(',i)
s=s[:i]+needle+'\n    return nbytes<0 ? -1 : sm64_naomi_save_read((unsigned)address*8,buffer,(unsigned)nbytes);\n}\n\n'+s[j:]
i=s.index('s32 osEepromLongWrite(');j=s.index('{',i)
# Last routine in this source file.
assert s[j:].rstrip().endswith('}')
s=s[:j+1]+'\n    return nbytes<0 ? -1 : sm64_naomi_save_write((unsigned)address*8,buffer,(unsigned)nbytes);\n}\n'
p.write_text(s)
p=r/'src/pc/gfx/gfx_dc.c';s=p.read_text()
s=s.replace('#include <assert.h>','#include <assert.h>\n#include <stdint.h>\n#include <malloc.h>\n#include <dc/pvr.h>\n#include <dc/sound/sound.h>\n#include <GL/gl.h>\n#include <GL/glkos.h>')
needle='static unsigned int frame_time = 0;'
extra='''
/* Read-only diagnostic counters, sampled by external tools. */
volatile uint32_t sm64_diag[12];
static uint64_t frame_begin_us, previous_end_us, deadline_us;
static unsigned frame_fraction;
'''
assert s.count(needle)==1;s=s.replace(needle,needle+extra)
s=s.replace('static bool gfx_dc_start_frame(void) {\n    return true;', 'static bool gfx_dc_start_frame(void) {\n    frame_begin_us=timer_us_gettime64();\n    return true;')
s=s.replace('static void gfx_dc_swap_buffers_begin(void) {\n    glKosSwapBuffers();','static void gfx_dc_swap_buffers_begin(void) {\n    sm64_diag[1]=(uint32_t)(timer_us_gettime64()-frame_begin_us);\n    glKosSwapBuffers();')
i=s.index('static void gfx_dc_swap_buffers_end(void) {');j=s.index('\n/* Idk what this is for? */',i)
s=s[:i]+'''
static void gfx_dc_swap_buffers_end(void) {
    uint64_t now=timer_us_gettime64();
    if(!deadline_us || now>deadline_us+100000)deadline_us=now;
    deadline_us+=33333;
    if(++frame_fraction==3){deadline_us++;frame_fraction=0;}
    while(now<deadline_us){
        uint64_t remain=deadline_us-now;
        if(remain>11000)thd_sleep((unsigned)((remain-10000)/1000));
        else __asm__ volatile ("nop"); /* scheduler ticks are 10 ms; finish to the us deadline */
        now=timer_us_gettime64();
    }
    sm64_diag[2]=previous_end_us?(uint32_t)(now-previous_end_us):0;
    previous_end_us=now;
    struct mallinfo mi=mallinfo();
    sm64_diag[3]=(uint32_t)mi.uordblks;
    GLint texture_free=0;
    glGetIntegerv(GL_FREE_TEXTURE_MEMORY_KOS,&texture_free);
    sm64_diag[4]=(uint32_t)texture_free;
    sm64_diag[5]=snd_mem_available();
    if(!sm64_diag[0]||sm64_diag[4]<sm64_diag[6])sm64_diag[6]=sm64_diag[4];
    if(!sm64_diag[0]||sm64_diag[5]<sm64_diag[7])sm64_diag[7]=sm64_diag[5];
    if(sm64_diag[3]>sm64_diag[8])sm64_diag[8]=sm64_diag[3];
    if(sm64_diag[1]>sm64_diag[9])sm64_diag[9]=sm64_diag[1];
    sm64_diag[0]++;
}
''' + s[j:]
p.write_text(s)
print('Applied experimental SRAM save, 30 Hz deadline and memory/frame counters')