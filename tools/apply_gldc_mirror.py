#!/usr/bin/env python3
"""Expose PowerVR mirrored repeat without duplicating textures."""
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('--root',required=True);r=Path(p.parse_args().root)
def change(file,old,new,count=1):
    p=r/file;s=p.read_text()
    assert s.count(old)==count,(file,old)
    p.write_text(s.replace(old,new))
change('GL/private.h','    GLubyte  uv_clamp;','    GLubyte  uv_clamp;\n    GLubyte  uv_flip;')
change('GL/texture.c','    txr->uv_clamp = 0;','    txr->uv_clamp = 0;\n    txr->uv_flip = GPU_UVFLIP_NONE;')
change('GL/state.c','context->txr.uv_flip = GPU_UVFLIP_NONE;','context->txr.uv_flip = tx1->uv_flip;')
for axis,mask in [('S','U'),('T','V')]:
    file=r/'GL/texture.c';s=file.read_text();start=s.index('            case GL_TEXTURE_WRAP_'+axis+':');end=s.index('\n                break;',start)
    chunk=s[start:end]
    chunk=chunk.replace('active->uv_clamp |= CLAMP_'+mask+';','active->uv_clamp |= CLAMP_'+mask+';\n                        active->uv_flip &= ~GPU_UVFLIP_'+mask+';')
    chunk=chunk.replace('active->uv_clamp &= ~CLAMP_'+mask+';','active->uv_clamp &= ~CLAMP_'+mask+';\n                        active->uv_flip &= ~GPU_UVFLIP_'+mask+';')
    chunk=chunk.replace('                switch(param) {','                switch(param) {\n                    case 0x8370: /* GL_MIRRORED_REPEAT */\n                        active->uv_clamp &= ~CLAMP_'+mask+';\n                        active->uv_flip |= GPU_UVFLIP_'+mask+';\n                        break;')
    file.write_text(s[:start]+chunk+s[end:])
print('Applied native PowerVR mirrored repeat')

change('GL/state.c',
       'context->txr.alpha = (GPUState.blend_enabled || GPUState.alpha_test_enabled) ? GPU_TXRALPHA_ENABLE : GPU_TXRALPHA_DISABLE;',
       'context->txr.alpha = (GPUState.blend_enabled || GPUState.alpha_test_enabled || tx1->env == GPU_TXRENV_DECAL) ? GPU_TXRALPHA_ENABLE : GPU_TXRALPHA_DISABLE;')
print('Preserved texture alpha for opaque DECAL materials')