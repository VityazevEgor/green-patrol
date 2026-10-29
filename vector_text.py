from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REGULAR = "C:/Windows/Fonts/arial.ttf"

_cache = {}

def get_font(bold=True):
    path = FONT_BOLD if bold else FONT_REGULAR
    if not os.path.exists(path):
        path = "C:/Windows/Fonts/tahoma.ttf"
    if path not in _cache:
        font = TTFont(path)
        glyph_set = font.getGlyphSet()
        cmap = font.getBestCmap()
        units_per_em = font["head"].unitsPerEm
        _cache[path] = (font, glyph_set, cmap, units_per_em)
    return _cache[path]

def text_path(text, x, y, font_size, fill="#ffffff", align="start", bold=True):
    font, glyph_set, cmap, units_per_em = get_font(bold)
    scale = font_size / units_per_em
    glyphs = []
    total_width = 0
    for ch in text:
        code = ord(ch)
        gname = cmap.get(code, ".notdef")
        glyph = glyph_set[gname]
        adv = glyph.width * scale
        glyphs.append((gname, adv))
        total_width += adv
    
    start_x = x
    if align == "middle":
        start_x = x - total_width / 2.0
    elif align == "end":
        start_x = x - total_width
        
    pen = SVGPathPen(glyph_set)
    cur_x = start_x
    for gname, adv in glyphs:
        trans = TransformPen(pen, (scale, 0, 0, -scale, cur_x, y))
        glyph = glyph_set[gname]
        glyph.draw(trans)
        cur_x += adv
        
    d = pen.getCommands()
    return f'<path d="{d}" fill="{fill}" />'

if __name__ == "__main__":
    p = text_path("ПРОВЕРКА", 100, 100, 20)
    print("Vector text module works! Path length:", len(p))
