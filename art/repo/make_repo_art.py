#!/usr/bin/env python3
# Generates the Oniscus repository artwork (CC BY-SA 4.0): README banners,
# the GitHub social preview, logo lockups and the avatar.
#
# Usage: python3 make_repo_art.py FONT_DIR
#   FONT_DIR holds Nunito.ttf and NotoSansMono.ttf (variable fonts from
#   github.com/google/fonts, SIL OFL). All text is converted to outlines,
#   so the SVGs do not depend on fonts installed on the viewer's machine.
# PNGs are rendered afterwards by render.mjs (Chromium via Playwright).
import os, re, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, '..', 'branding')
FONTS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'fonts')

# Palette (see ../branding/README.md)
YELLOW, HONEY, AMBER, BEAK, SHELL, MOSS = '#F7C948', '#FFE58F', '#C99412', '#F28C28', '#4E3527', '#4CC27A'
GREY, CHARCOAL, GRAPHITE, SLATE, BORDER, MIST = '#9AA4AF', '#121519', '#1C2026', '#2A3038', '#3A424C', '#E6E9EC'
PAPER, INK, INK2 = '#FBF7EC', '#121519', '#55606B'  # light-mode background and text

_fonts = {}
def font(name, wght):
    key = (name, wght)
    if key not in _fonts:
        f = TTFont(os.path.join(FONTS, name + '.ttf'))
        axes = {'wght': wght}
        if 'wdth' in [a.axisTag for a in f['fvar'].axes]:
            axes['wdth'] = 100
        _fonts[key] = instantiateVariableFont(f, axes)
    return _fonts[key]

def text_path(text, name, wght, size, x, y, fill, anchor='start', track=0.0):
    """Returns (svg <path>, width) for text set on baseline y."""
    f = font(name, wght)
    upm = f['head'].unitsPerEm
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f['hmtx']
    s = size / upm
    width = sum(hmtx[cmap[ord(c)]][0] for c in text) * s + track * size * (len(text) - 1)
    if anchor == 'middle':
        x -= width / 2
    elif anchor == 'end':
        x -= width
    pen = SVGPathPen(gs)
    cx = x
    for c in text:
        g = cmap[ord(c)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += hmtx[g][0] * s + track * size
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>', width

def mascot_src(icon=False):
    s = open(os.path.join(BRAND, 'oniscus-mascot-icon.svg' if icon else 'oniscus-mascot.svg')).read()
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = s[s.index('>') + 1:s.rindex('</svg>')]
    return vb, inner

def mascot(x, y, w, prefix, icon=False, flip=False):
    """The approved mascot, unchanged, placed in a w-wide box at (x, y)."""
    vb, inner = mascot_src(icon)
    for i in set(re.findall(r'id="([^"]+)"', inner)):
        inner = inner.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f'url(#{i})', f'url(#{prefix}{i})')
    vx, vy, vw, vh = map(float, vb.split())
    h = w * vh / vw
    g = f'<svg x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" viewBox="{vb}">{inner}</svg>'
    if flip:
        g = f'<g transform="translate({2 * x + w:.1f} 0) scale(-1 1)">{g}</g>'
    return g, h

def doc(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<title>{title}</title>{body}</svg>\n')

def shell_arcs(cx, cy, r0, n, step, col, op, sw=2):
    """Concentric arcs echoing the segments of the shell (background motif)."""
    return ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r0 + i * step}" fill="none" stroke="{col}" '
                   f'stroke-width="{sw}" opacity="{op * (1 - i / n):.3f}"/>' for i in range(n))

def background(w, h, dark, pid):
    if dark:
        return (f'<defs><radialGradient id="{pid}g1" cx="0.78" cy="0.5" r="0.6">'
                f'<stop offset="0" stop-color="{AMBER}" stop-opacity="0.28"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
                f'<radialGradient id="{pid}g2" cx="0.1" cy="1" r="0.7">'
                f'<stop offset="0" stop-color="{SHELL}" stop-opacity="0.55"/><stop offset="1" stop-color="{SHELL}" stop-opacity="0"/></radialGradient>'
                f'<clipPath id="{pid}c"><rect width="{w}" height="{h}" rx="{24 if w < 1280 or h < 640 else 0}"/></clipPath></defs>'
                f'<g clip-path="url(#{pid}c)"><rect width="{w}" height="{h}" fill="{CHARCOAL}"/>'
                f'<rect width="{w}" height="{h}" fill="url(#{pid}g2)"/><rect width="{w}" height="{h}" fill="url(#{pid}g1)"/>')
    return (f'<defs><radialGradient id="{pid}g1" cx="0.78" cy="0.5" r="0.6">'
            f'<stop offset="0" stop-color="{YELLOW}" stop-opacity="0.35"/><stop offset="1" stop-color="{YELLOW}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="{pid}c"><rect width="{w}" height="{h}" rx="24"/></clipPath></defs>'
            f'<g clip-path="url(#{pid}c)"><rect width="{w}" height="{h}" fill="{PAPER}"/>'
            f'<rect width="{w}" height="{h}" fill="url(#{pid}g1)"/>')

def pill(x, y, text, dark, size=22):
    """Terminal-style pill: '$ onis' in Noto Sans Mono."""
    p1, w1 = text_path('$', 'NotoSansMono', 600, size, 0, 0, YELLOW if dark else AMBER)
    p2, w2 = text_path(text, 'NotoSansMono', 500, size, 0, 0, MIST if dark else INK)
    pad, gap, hh = size * 0.8, size * 0.6, size * 2
    w = pad * 2 + w1 + gap + w2
    base = y + hh / 2 + size * 0.36
    a, _ = text_path('$', 'NotoSansMono', 600, size, x + pad, base, YELLOW if dark else AMBER)
    b, _ = text_path(text, 'NotoSansMono', 500, size, x + pad + w1 + gap, base, MIST if dark else INK)
    box = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{hh}" rx="{hh / 2}" '
           f'fill="{SLATE if dark else "#FFFFFF"}" stroke="{BORDER if dark else "#E4DCC6"}" stroke-width="1.5"/>')
    return box + a + b, w

TAG_EN = 'A cozy Linux that just works'
TAG_PT = 'Um Linux aconchegante que simplesmente funciona'

def banner(dark, w=1280, h=400, tagline=TAG_EN):
    pid = 'd' if dark else 'l'
    fg, fg2 = (MIST, GREY) if dark else (INK, INK2)
    body = background(w, h, dark, pid)
    body += shell_arcs(w * 0.80, h * 0.62, 150, 6, 46, BORDER if dark else '#E8D9A8', 0.9)
    m, mh = mascot(w * 0.80 - 190, h * 0.56 - 140, 380, pid + 'm')
    body += m
    word, ww = text_path('Oniscus', 'Nunito', 900, 132, 88, 205, fg, track=-0.01)
    body += word
    tag, _ = text_path(tagline, 'Nunito', 600, 30, 92, 262, fg2)
    body += tag
    pl, _ = pill(90, 300, 'onis', dark)
    body += pl + '</g>'
    return doc(w, h, body, 'Oniscus')

def social(w=1280, h=640):
    # GitHub crops the edges in some places: keep content inside 40 px.
    body = background(w, h, True, 's')
    body += shell_arcs(w * 0.77, h * 0.56, 190, 7, 52, BORDER, 0.9)
    m, mh = mascot(w * 0.77 - 260, h * 0.52 - 190, 520, 'sm')
    body += m
    word, ww = text_path('Oniscus', 'Nunito', 900, 150, 96, 330, MIST, track=-0.01)
    body += word
    t1, _ = text_path('A cozy Linux that just works', 'Nunito', 700, 40, 100, 400, MIST)
    t2, _ = text_path('openSUSE Tumbleweed base · XFCE + i3', 'Nunito', 600, 30, 100, 448, GREY)
    pl, _ = pill(98, 488, 'onis', True, 24)
    url, _ = text_path('github.com/arthurcvieira/oniscus', 'NotoSansMono', 500, 22, 100, 596, GREY)
    body += t1 + t2 + pl + url
    body += f'<rect x="0" y="{h - 10}" width="{w}" height="10" fill="{YELLOW}"/></g>'
    return doc(w, h, body, 'Oniscus')

def lockup(dark):
    """Horizontal logo: mascot + wordmark, transparent background."""
    fg = MIST if dark else INK
    m, mh = mascot(0, 0, 200, 'k')
    word, ww = text_path('Oniscus', 'Nunito', 900, 112, 222, 112, fg, track=-0.01)
    w = int(222 + ww + 6)
    return doc(w, int(mh), m + word, 'Oniscus')

def wordmark(dark):
    fg = MIST if dark else INK
    word, ww = text_path('Oniscus', 'Nunito', 900, 112, 4, 112, fg, track=-0.01)
    return doc(int(ww + 8), 140, word, 'Oniscus')

def avatar(size=512):
    m, mh = mascot(size * 0.08, size * 0.08, size * 0.84, 'a', icon=True)
    body = (f'<defs><radialGradient id="ag" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="{GRAPHITE}"/>'
            f'<stop offset="1" stop-color="{CHARCOAL}"/></radialGradient></defs>'
            f'<rect width="{size}" height="{size}" fill="url(#ag)"/>'
            + shell_arcs(size / 2, size * 0.56, size * 0.3, 4, size * 0.08, BORDER, 0.7) + m)
    return doc(size, size, body, 'Oniscus')

def divider(w=1280, h=24):
    """Thin section divider for long READMEs: yellow dots fading out."""
    dots = ''.join(f'<circle cx="{w / 2 + d * 22}" cy="{h / 2}" r="{4 - abs(d) * 0.6:.1f}" fill="{YELLOW}" '
                   f'opacity="{1 - abs(d) * 0.18:.2f}"/>' for d in range(-4, 5))
    line = (f'<rect x="{w * 0.12}" y="{h / 2 - 0.75}" width="{w * 0.76}" height="1.5" fill="{BORDER}" opacity="0.8"/>')
    return doc(w, h, line + dots, 'divider')

if __name__ == '__main__':
    out = HERE
    files = {
        'banner-dark.svg': banner(True),
        'banner-light.svg': banner(False),
        'banner-dark.pt-BR.svg': banner(True, tagline=TAG_PT),
        'banner-light.pt-BR.svg': banner(False, tagline=TAG_PT),
        'social-preview.svg': social(),
        'logo-horizontal-dark.svg': lockup(True),
        'logo-horizontal-light.svg': lockup(False),
        'wordmark-dark.svg': wordmark(True),
        'wordmark-light.svg': wordmark(False),
        'avatar.svg': avatar(),
        'divider.svg': divider(),
    }
    for name, svg in files.items():
        with open(os.path.join(out, name), 'w') as fh:
            fh.write(svg)
        print(name)
