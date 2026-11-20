from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("component", choices=("gldc", "sm64"))
parser.add_argument("root", type=Path)
args = parser.parse_args()

def replace(source, old, new):
    if source.count(old) != 1:
        raise SystemExit("Unexpected patch site: " + old[:100])
    return source.replace(old, new, 1)

if args.component == "sm64":
    path = args.root / "src/pc/gfx/gfx_gldc.c"
    source = path.read_text()
    source = replace(source, "    glBindTexture(GL_TEXTURE_2D, texture_id);\n}\n/* Used for rescaling",
        """    glBindTexture(GL_TEXTURE_2D, texture_id);
    /* GLdc stores texenv on the bound texture. Apply the current combiner
       again when a display list switches textures without changing shaders. */
    if (cur_shader)
        cur_shader->enabled = false;
}
/* Used for rescaling""")
    path.write_text(source)
else:
    path = args.root / "GL/draw.c"
    source = path.read_text()
    marker = "    // /*\n    //    Now, if multitexturing is enabled,"
    addition = """    /* PowerVR uses reciprocal clip W as depth in perspective mode.
       Apply a small relative depth bias to depth-tested, non-writing
       surface decals. Rescaling all four clip coordinates together preserves
       projected XY, clipping ratios, and perspective-correct interpolation. */
    if (_glIsDepthTestEnabled() && !_glIsDepthWriteEnabled()
        && glIsEnabled(GL_POLYGON_OFFSET_FILL)) {
        GLfloat units = 0.0f;
        glGetFloatv(GL_POLYGON_OFFSET_UNITS, &units);
        if (units < 0.0f) {
            const GLfloat scale = 1.0f + MAX(units, -8.0f) * (1.0f / 4096.0f);
            Vertex *vertex = _glSubmissionTargetStart(target);
            for (uint32_t i = 0; i < target->count; ++i, ++vertex) {
                if (vertex->w > 1.0f) {
                    vertex->xyz[0] *= scale;
                    vertex->xyz[1] *= scale;
                    vertex->xyz[2] *= scale;
                    vertex->w *= scale;
                }
            }
        }
    }

"""
    path.write_text(replace(source, marker, addition + marker))
