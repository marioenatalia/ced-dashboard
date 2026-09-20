#!/usr/bin/env python3
"""Genera l'artwork SVG dei prodotti Vera Candles.

Illustrazioni vettoriali eleganti (nessuna dipendenza esterna, nessuna foto):
fondale sfumato, alone di luce, ombra morbida, vetro/cera in trasparenza.
Servono da placeholder di pregio finche' non arrivano le foto reali.
"""
import os, math

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)

W, H = 800, 1000


def head(uid, bg1, bg2, glow):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="{bg1}"/><stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <radialGradient id="glow{uid}" cx="50%" cy="42%" r="52%">
      <stop offset="0%" stop-color="{glow}" stop-opacity=".85"/>
      <stop offset="60%" stop-color="{glow}" stop-opacity=".18"/>
      <stop offset="100%" stop-color="{glow}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="wax{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000" stop-opacity=".16"/>
      <stop offset="22%" stop-color="#fff" stop-opacity=".30"/>
      <stop offset="55%" stop-color="#fff" stop-opacity=".05"/>
      <stop offset="100%" stop-color="#000" stop-opacity=".20"/>
    </linearGradient>
    <radialGradient id="flame{uid}" cx="50%" cy="70%" r="60%">
      <stop offset="0%" stop-color="#FFF6DA"/><stop offset="45%" stop-color="#FFD98A"/>
      <stop offset="100%" stop-color="#E9A94B" stop-opacity="0"/>
    </radialGradient>
    <filter id="soft{uid}" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="grain{uid}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="{uid}"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg{uid})"/>
  <rect width="{W}" height="{H}" fill="url(#glow{uid})"/>
'''


def tail(uid):
    return f'''  <rect width="{W}" height="{H}" filter="url(#grain{uid})" opacity=".05" style="mix-blend-mode:multiply"/>
  <rect x="0" y="0" width="{W}" height="{H}" fill="none"/>
</svg>
'''


def shadow(uid, cx, cy, rx, ry, o=".18"):
    return (f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#3A2E24" opacity="{o}"'
            f' filter="url(#soft{uid})"/>\n')


def flame(uid, cx, base, scale=1.0):
    h = 62 * scale
    w = 20 * scale
    return (f'  <ellipse cx="{cx}" cy="{base - h*0.55:.0f}" rx="{w*2.6:.0f}" ry="{h*1.5:.0f}"'
            f' fill="url(#flame{uid})" opacity=".55"/>\n'
            f'  <path d="M {cx} {base - h:.1f} C {cx + w:.1f} {base - h*0.55:.1f}, {cx + w*0.75:.1f} {base:.1f}, {cx} {base:.1f}'
            f' C {cx - w*0.75:.1f} {base:.1f}, {cx - w:.1f} {base - h*0.55:.1f}, {cx} {base - h:.1f} Z"'
            f' fill="#FFE0A0" opacity=".95"/>\n'
            f'  <path d="M {cx} {base - h*0.62:.1f} C {cx + w*0.4:.1f} {base - h*0.3:.1f}, {cx + w*0.3:.1f} {base - h*0.05:.1f}, {cx} {base - h*0.05:.1f}'
            f' C {cx - w*0.3:.1f} {base - h*0.05:.1f}, {cx - w*0.4:.1f} {base - h*0.3:.1f}, {cx} {base - h*0.62:.1f} Z"'
            f' fill="#FFFBEF" opacity=".9"/>\n')


def wick(cx, base, h=16):
    """Stoppino: parte dalla cera e sale; la fiamma, disegnata dopo, lo copre."""
    return (f'  <path d="M {cx} {base} q 4 {-h*0.45:.0f} 0 {-h}" stroke="#4A3B2E" stroke-width="3.2"'
            f' fill="none" stroke-linecap="round" opacity=".75"/>\n')


# ---------------------------------------------------------------- varianti ---
def v_pillar(uid, c, accent):
    """Candela colonna scanalata su base di pietra."""
    s = ''
    cx, top, bot, w = 400, 300, 760, 150
    s += shadow(uid, cx, bot + 26, w * 1.35, 34)
    # base / piedistallo
    s += f'  <rect x="{cx-w*1.5:.0f}" y="{bot}" width="{w*3:.0f}" height="34" rx="6" fill="{accent}" opacity=".55"/>\n'
    s += f'  <rect x="{cx-w:.0f}" y="{top}" width="{w*2:.0f}" height="{bot-top}" rx="14" fill="{c}"/>\n'
    for i in range(1, 10):
        x = cx - w + (2 * w) * i / 10
        s += (f'  <line x1="{x:.0f}" y1="{top+16}" x2="{x:.0f}" y2="{bot-14}" stroke="#fff"'
              f' stroke-opacity=".16" stroke-width="7"/>\n')
    s += f'  <rect x="{cx-w:.0f}" y="{top}" width="{w*2:.0f}" height="{bot-top}" rx="14" fill="url(#wax{uid})"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top}" rx="{w}" ry="26" fill="{c}"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top}" rx="{w}" ry="26" fill="#fff" opacity=".22"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top+4}" rx="{w*0.55:.0f}" ry="13" fill="#000" opacity=".10"/>\n'
    s += wick(cx, top - 2)
    s += flame(uid, cx, top - 12, 1.15)
    return s


def v_bowl(uid, c, accent):
    """Coppa bassa a tre stoppini."""
    s = ''
    cx, top, bot, w = 400, 470, 700, 215
    s += shadow(uid, cx, bot + 20, w * 1.15, 30)
    s += (f'  <path d="M {cx-w} {top} L {cx-w*0.72:.0f} {bot} Q {cx} {bot+52} {cx+w*0.72:.0f} {bot}'
          f' L {cx+w} {top} Z" fill="{c}"/>\n')
    s += (f'  <path d="M {cx-w} {top} L {cx-w*0.72:.0f} {bot} Q {cx} {bot+52} {cx+w*0.72:.0f} {bot}'
          f' L {cx+w} {top} Z" fill="url(#wax{uid})"/>\n')
    s += f'  <ellipse cx="{cx}" cy="{top}" rx="{w}" ry="42" fill="{accent}" opacity=".9"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top+8}" rx="{w-16}" ry="34" fill="#000" opacity=".12"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top+6}" rx="{w-26}" ry="28" fill="#fff" opacity=".18"/>\n'
    for dx, sc in ((-88, .85), (0, 1.0), (92, .8)):
        s += wick(cx + dx, top - 2, 20)
        s += flame(uid, cx + dx, top - 10, sc)
    return s


def v_jar(uid, c, accent):
    """Vaso in vetro rigato con cera in trasparenza."""
    s = ''
    cx, top, bot, w = 400, 360, 730, 168
    s += shadow(uid, cx, bot + 22, w * 1.25, 30)
    s += f'  <rect x="{cx-w:.0f}" y="{top}" width="{w*2:.0f}" height="{bot-top}" rx="18" fill="{c}" opacity=".92"/>\n'
    # cera interna
    s += f'  <rect x="{cx-w+18:.0f}" y="{top+70}" width="{w*2-36:.0f}" height="{bot-top-88}" rx="12" fill="{accent}" opacity=".85"/>\n'
    for i in range(1, 12):
        x = cx - w + (2 * w) * i / 12
        s += (f'  <line x1="{x:.0f}" y1="{top+10}" x2="{x:.0f}" y2="{bot-10}" stroke="#fff"'
              f' stroke-opacity=".20" stroke-width="5"/>\n')
    s += f'  <rect x="{cx-w:.0f}" y="{top}" width="{w*2:.0f}" height="{bot-top}" rx="18" fill="url(#wax{uid})"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top}" rx="{w}" ry="30" fill="{c}"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top}" rx="{w-14}" ry="22" fill="#000" opacity=".14"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top+72}" rx="{w-20}" ry="22" fill="{accent}"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top+72}" rx="{w-20}" ry="22" fill="#fff" opacity=".16"/>\n'
    for dx in (-58, 58):
        s += wick(cx + dx, top + 66, 18)
        s += flame(uid, cx + dx, top + 58, .8)
    return s


def v_sculpture(uid, c, accent):
    """Candela scultura: corpo organico a doppia curva."""
    s = ''
    cx, top, bot = 400, 250, 740
    s += shadow(uid, cx, bot + 24, 210, 32)
    s += f'  <ellipse cx="{cx}" cy="{bot}" rx="150" ry="34" fill="{accent}" opacity=".55"/>\n'
    body = (f'M {cx-70} {bot} C {cx-190} {bot-140}, {cx+60} {bot-210}, {cx-40} {bot-330} '
            f'C {cx-110} {bot-420}, {cx+70} {bot-430}, {cx+18} {top+20} '
            f'C {cx+130} {top+150}, {cx+140} {bot-160}, {cx+70} {bot} Z')
    s += f'  <path d="{body}" fill="{c}"/>\n'
    s += f'  <path d="{body}" fill="url(#wax{uid})"/>\n'
    s += (f'  <path d="M {cx-30} {bot-60} C {cx-90} {bot-200}, {cx+40} {bot-280}, {cx-14} {top+90}"'
          f' stroke="#fff" stroke-opacity=".22" stroke-width="16" fill="none" stroke-linecap="round"/>\n')
    s += wick(cx + 16, top + 14, 22)
    s += flame(uid, cx + 16, top + 6, 1.05)
    return s


def v_tapers(uid, c, accent):
    """Trittico di candele affusolate."""
    s = ''
    bot = 730
    s += shadow(uid, 400, bot + 22, 250, 30)
    for dx, hh, ww, col in ((-140, 300, 26, accent), (0, 400, 30, c), (140, 250, 24, c)):
        cx = 400 + dx
        top = bot - hh
        s += (f'  <rect x="{cx-46:.0f}" y="{bot-6}" width="92" height="26" rx="8" fill="{accent}" opacity=".65"/>\n')
        s += (f'  <path d="M {cx-ww} {bot} L {cx-ww*0.62:.0f} {top+18} Q {cx} {top-6} {cx+ww*0.62:.0f} {top+18}'
              f' L {cx+ww} {bot} Z" fill="{col}"/>\n')
        s += (f'  <path d="M {cx-ww} {bot} L {cx-ww*0.62:.0f} {top+18} Q {cx} {top-6} {cx+ww*0.62:.0f} {top+18}'
              f' L {cx+ww} {bot} Z" fill="url(#wax{uid})"/>\n')
        s += wick(cx, top - 4, 18)
        s += flame(uid, cx, top - 12, .78)
    return s


def v_sphere(uid, c, accent):
    """Sfera di cera su plinto."""
    s = ''
    cx, cy, r = 400, 500, 190
    s += shadow(uid, cx, cy + r + 34, 200, 28)
    s += f'  <rect x="{cx-104}" y="{cy+r-16}" width="208" height="44" rx="8" fill="{accent}" opacity=".7"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{cy+r-16}" rx="104" ry="12" fill="#fff" opacity=".18"/>\n'
    s += f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>\n'
    s += f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#wax{uid})"/>\n'
    s += f'  <ellipse cx="{cx-58}" cy="{cy-72}" rx="62" ry="46" fill="#fff" opacity=".22"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{cy+r-14}" rx="{r*0.55:.0f}" ry="24" fill="#000" opacity=".10"/>\n'
    s += wick(cx, cy - r + 2, 22)
    s += flame(uid, cx, cy - r - 6, 1.0)
    return s


VARIANTS = {
    'pillar': v_pillar, 'bowl': v_bowl, 'jar': v_jar,
    'sculpture': v_sculpture, 'tapers': v_tapers, 'sphere': v_sphere,
}

# nome file, variante, bg1, bg2, glow, colore cera, accento
PIECES = [
    ("notte-di-seta",     'sculpture', "#20191B", "#3A2A2C", "#C98B62", "#E9D9CF", "#B4885E"),
    ("oro-bianco",        'pillar',    "#F4EDE4", "#E4D7C6", "#F6E3BC", "#FBF4E8", "#C9A66B"),
    ("giardino-privato",  'bowl',      "#EDEDE4", "#DCDFD2", "#EDE3C4", "#E7EADC", "#A8A98F"),
    ("ambra-rara",        'jar',       "#F1E5D8", "#DFCAB2", "#F2CE97", "#E8C79B", "#C08A4E"),
    ("veneziana",         'tapers',    "#EFE7EA", "#DCC9CF", "#F0D6C9", "#EBD2D3", "#B58A8C"),
    ("luna-piena",        'sphere',    "#E9E9EE", "#D3D4DE", "#EDE6F1", "#EFEDE9", "#9C99A8"),
    ("terra-di-siena",    'pillar',    "#F2E9DF", "#DDCBB9", "#EFD3A9", "#D9B08C", "#9E6B45"),
    ("prima-neve",        'bowl',      "#F7F4F0", "#E8E3DC", "#F7ECD9", "#FAF7F2", "#D8CFC2"),
    ("rosa-antica",       'jar',       "#F3E9E7", "#E1CDC9", "#F3D9CE", "#E6C8C1", "#B98A7D"),
    ("mezzanotte",        'sculpture', "#181C22", "#2C333D", "#8EA6C4", "#D7DEE8", "#7C8CA3"),
]


def main():
    for i, (name, var, bg1, bg2, glow, wax, accent) in enumerate(PIECES, start=1):
        svg = head(i, bg1, bg2, glow) + VARIANTS[var](i, wax, accent) + tail(i)
        with open(os.path.join(OUT, f"{name}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        print("ok", name)


if __name__ == "__main__":
    main()
