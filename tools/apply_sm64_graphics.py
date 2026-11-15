#!/usr/bin/env python3
"""Apply guarded GLdc fidelity corrections to the pinned Dreamcast backend."""
import os
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('--upstream',required=True);a=p.parse_args()
root=Path(a.upstream);stage=os.environ.get('SM64_GRAPHICS_STAGE','full')
g=root/'src/pc/gfx/gfx_gldc.c';s=g.read_text()
before='''    if(cur_shader->shader_id == 0x1200045){ // 0x1200045, skybox
        //glDepthMask(false);
        return; // Sky seems to always draw on top?
    }

    glDrawArrays(GL_TRIANGLES, 0, 3 * buf_vbo_num_tris);

    if(cur_shader->shader_id == 0x1200045){ // 0x1200045, skybox
        //glDepthMask(true);
    }'''
after='''    /* F3DEX2 skybox: opaque background, no Z writes. GLdc otherwise queues
       this fully opaque material with translucent geometry, drawing it last.
       Preserve the frontend state after submitting to the opaque list. */
    const bool skybox = cur_shader->shader_id == 0x01200045;
    if (skybox) glDisable(GL_BLEND);
    glDrawArrays(GL_TRIANGLES, 0, 3 * buf_vbo_num_tris);
    if (skybox && gl_blend) glEnable(GL_BLEND);'''
assert s.count(before)==1,'skybox patch point changed'
s=s.replace(before,after)
if stage != 'sky':
    # G_CC_BLENDRGBFADEA uses the same RGB equation as BLENDRGB, but a
    # different alpha combiner. Match the RGB operation, not a whole shader ID.
    needle = '    GLenum mode;\n\n    // HACK:'
    replacement = '''    if (prg->cc.do_mix[0] &&
        prg->cc.c[0][0] == SHADER_TEXEL0 &&
        prg->cc.c[0][2] == SHADER_TEXEL0A)
        return GL_DECAL;
    GLenum mode;

    // HACK:'''
    assert s.count(needle) == 1
    s = s.replace(needle, replacement)
old = '    return  GL_REPEAT;'
assert s.count(old) == 1
s = s.replace(old, '    return (val & G_TX_MIRROR) ? 0x8370 /* GL_MIRRORED_REPEAT */ : GL_REPEAT;')
g.write_text(s)
if stage != 'sky':
    f=root/'src/pc/gfx/gfx_retro_dc.c';t=f.read_text()
    for fn,alpha in [('import_texture_i4','SCALE_4_8(intensity)'),('import_texture_i8','intensity')]:
        start=t.index('static void '+fn+'(');end=t.index('\nstatic void ',start+1)
        chunk=t[start:end]
        assert chunk.count('rgba32_buf[4*i + 3] = 255;') == 1
        chunk=chunk.replace('rgba32_buf[4*i + 3] = 255;','rgba32_buf[4*i + 3] = '+alpha+';')
        t=t[:start]+chunk+t[end:]
    start=t.index('        int j, k;',t.index('static void gfx_sp_tri1('))
    end=t.index('        /*@Error: Transition Hack */',start)
    t=t[:start]+'''        /* Fixed-function RGB and alpha inputs are independent. The old loop
           overwrote RGB with later inputs and never selected the alpha source. */
        struct RGBA color = {255, 255, 255, 255};
        switch (comb->shader_input_mapping[0][0]) {
            case CC_PRIM: color = rdp.prim_color; break;
            case CC_SHADE: color = v_arr[i]->color; break;
            case CC_ENV: color = rdp.env_color; break;
            case CC_LOD: {
                float f = (v1->w - 3000.0f) / 3000.0f;
                if (f < 0) f = 0; if (f > 1) f = 1;
                color.r = color.g = color.b = (uint8_t)(f * 255);
                break;
            }
        }
        color.a = 255;
        if (use_alpha) {
            switch (comb->shader_input_mapping[1][0]) {
                case CC_PRIM: color.a = rdp.prim_color.a; break;
                case CC_SHADE: color.a = v_arr[i]->color.a; break;
                case CC_ENV: color.a = rdp.env_color.a; break;
            }
        }
        buf_vbo[buf_num_vert].color.packed =
            PACK_ARGB8888(color.r, color.g, color.b, color.a);
''' + t[end:]
    f.write_text(t)
print('Applied graphics stage:',stage)
# Restore original N64 shadow UVs. The DC base had reduced -15..15 to
# 0..15 to work around absent mirrored-repeat, leaving one quadrant.
f=root/'src/game/shadow.c';t=f.read_text()
for old,new in [
 ('(vertexNum % 3) * 8 - !((vertexNum % 3) == 0)', '(vertexNum % 3) * 15 - 15'),
 ('(vertexNum / 3) * 8 - !((vertexNum / 3) == 0)', '(vertexNum / 3) * 15 - 15'),
 ('(vertexNum % 2) * 15', '(vertexNum % 2) * 30 - 15'),
 ('(vertexNum / 2) * 15', '(vertexNum / 2) * 30 - 15')]:
    assert t.count(old)==1,old
    t=t.replace(old,new)
f.write_text(t)
print('Restored original shadow UV range')