#!/usr/bin/env python3
"""Immagini editoriali SVG per Vera Candles (hero, atelier, rituale, su misura)."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)


def defs(uid, bg1, bg2, glow, gx="46%", gy="52%", gr="58%"):
    return f'''  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2=".25" y2="1">
      <stop offset="0%" stop-color="{bg1}"/><stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <radialGradient id="glow{uid}" cx="{gx}" cy="{gy}" r="{gr}">
      <stop offset="0%" stop-color="{glow}" stop-opacity=".9"/>
      <stop offset="45%" stop-color="{glow}" stop-opacity=".26"/>
      <stop offset="100%" stop-color="{glow}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000" stop-opacity=".35"/>
      <stop offset="30%" stop-color="#fff" stop-opacity=".22"/>
      <stop offset="70%" stop-color="#fff" stop-opacity=".04"/>
      <stop offset="100%" stop-color="#000" stop-opacity=".38"/>
    </linearGradient>
    <radialGradient id="fl{uid}" cx="50%" cy="70%" r="60%">
      <stop offset="0%" stop-color="#FFF7E2"/><stop offset="45%" stop-color="#FFD98A"/>
      <stop offset="100%" stop-color="#E9A94B" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vig{uid}" cx="50%" cy="50%" r="72%">
      <stop offset="55%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity=".5"/>
    </radialGradient>
    <filter id="soft{uid}" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="22"/></filter>
    <filter id="grain{uid}"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="{uid}"/><feColorMatrix type="saturate" values="0"/></filter>
  </defs>
'''


def flame(uid, cx, base, s=1.0):
    h, w = 62 * s, 20 * s
    return (f'  <ellipse cx="{cx}" cy="{base-h*.55:.0f}" rx="{w*3:.0f}" ry="{h*1.7:.0f}" fill="url(#fl{uid})" opacity=".5"/>\n'
            f'  <path d="M {cx} {base-h:.1f} C {cx+w:.1f} {base-h*.55:.1f}, {cx+w*.75:.1f} {base:.1f}, {cx} {base:.1f}'
            f' C {cx-w*.75:.1f} {base:.1f}, {cx-w:.1f} {base-h*.55:.1f}, {cx} {base-h:.1f} Z" fill="#FFE6B4" opacity=".95"/>\n'
            f'  <path d="M {cx} {base-h*.6:.1f} C {cx+w*.38:.1f} {base-h*.3:.1f}, {cx+w*.3:.1f} {base-h*.05:.1f}, {cx} {base-h*.05:.1f}'
            f' C {cx-w*.3:.1f} {base-h*.05:.1f}, {cx-w*.38:.1f} {base-h*.3:.1f}, {cx} {base-h*.6:.1f} Z" fill="#FFFCF2"/>\n')


def wick(cx, base, h=15):
    """Stoppino che sale dalla cera: la fiamma, disegnata dopo, lo copre quasi tutto."""
    return f'  <path d="M {cx} {base} q 4 {-h*.45:.0f} 0 {-h}" stroke="#3A2E22" stroke-width="2.8" fill="none" stroke-linecap="round" opacity=".8"/>\n'


def pillar(uid, cx, top, bot, w, col, ribs=True):
    s = f'  <rect x="{cx-w}" y="{top}" width="{2*w}" height="{bot-top}" rx="10" fill="{col}"/>\n'
    if ribs:
        for i in range(1, 7):
            x = cx - w + 2 * w * i / 7
            s += f'  <line x1="{x:.0f}" y1="{top+12}" x2="{x:.0f}" y2="{bot-10}" stroke="#fff" stroke-opacity=".10" stroke-width="6"/>\n'
    s += f'  <rect x="{cx-w}" y="{top}" width="{2*w}" height="{bot-top}" rx="10" fill="url(#rim{uid})"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top}" rx="{w}" ry="{max(8, w*.24):.0f}" fill="{col}"/>\n'
    s += f'  <ellipse cx="{cx}" cy="{top}" rx="{w}" ry="{max(8, w*.24):.0f}" fill="#fff" opacity=".14"/>\n'
    s += wick(cx, top - 2) + flame(uid, cx, top - 10, 1.0 + w / 300)
    return s


def taper(uid, cx, top, bot, w, col):
    s = (f'  <path d="M {cx-w} {bot} L {cx-w*.6:.0f} {top+16} Q {cx} {top-4} {cx+w*.6:.0f} {top+16} L {cx+w} {bot} Z" fill="{col}"/>\n'
         f'  <path d="M {cx-w} {bot} L {cx-w*.6:.0f} {top+16} Q {cx} {top-4} {cx+w*.6:.0f} {top+16} L {cx+w} {bot} Z" fill="url(#rim{uid})"/>\n')
    s += wick(cx, top - 4, 18) + flame(uid, cx, top - 12, .75)
    return s


def shadow(uid, cx, cy, rx, ry, o=".4"):
    return f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#0B0806" opacity="{o}" filter="url(#soft{uid})"/>\n'


def grain(uid, w, h, o=".06"):
    return f'  <rect width="{w}" height="{h}" filter="url(#grain{uid})" opacity="{o}" style="mix-blend-mode:overlay"/>\n'


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMidYMid slice" role="img">\n{body}</svg>\n')


# --------------------------------------------------------------- hero ---
def hero():
    uid, W, H = 21, 1600, 1000
    line = 720
    s = defs(uid, "#17120E", "#2B2019", "#E0A65C", gx="42%", gy="46%", gr="55%")
    s += f'  <rect width="{W}" height="{H}" fill="url(#bg{uid})"/>\n'
    s += f'  <rect width="{W}" height="{H}" fill="url(#glow{uid})"/>\n'
    # parete di fondo appena piu' chiara
    s += f'  <rect x="0" y="0" width="{W}" height="{line}" fill="#000" opacity=".10"/>\n'
    # piano
    s += f'  <rect x="0" y="{line}" width="{W}" height="{H-line}" fill="#120D0A" opacity=".55"/>\n'
    s += f'  <line x1="0" y1="{line}" x2="{W}" y2="{line}" stroke="#E0A65C" stroke-opacity=".18" stroke-width="2"/>\n'
    # ombre
    for cx, rx in ((520, 210), (760, 120), (1030, 170), (1210, 90)):
        s += shadow(uid, cx, line + 26, rx, 26)
    # candele
    s += pillar(uid, 520, 388, line + 6, 96, "#E7D6C2")
    s += taper(uid, 760, 300, line + 4, 20, "#D9C3A8")
    s += pillar(uid, 1030, 470, line + 6, 74, "#C9A981", ribs=False)
    s += taper(uid, 1210, 430, line + 4, 17, "#EADCC8")
    # polvere sospesa
    for x, y, r, o in ((300, 250, 3, .22), (640, 190, 2, .18), (900, 300, 3, .16),
                       (1290, 240, 2, .2), (1420, 380, 3, .14), (200, 430, 2, .16)):
        s += f'  <circle cx="{x}" cy="{y}" r="{r}" fill="#F6E2C0" opacity="{o}"/>\n'
    s += f'  <rect width="{W}" height="{H}" fill="url(#vig{uid})"/>\n'
    s += grain(uid, W, H, ".07")
    return svg(W, H, s)


# ------------------------------------------------------- editoriali ---
def atelier():
    """Scaffale dell'atelier: vasi allineati in luce calda."""
    uid, W, H = 22, 1000, 1250
    s = defs(uid, "#F0E7DA", "#DFCFBB", "#F7DFB4", gx="50%", gy="38%", gr="62%")
    s += f'  <rect width="{W}" height="{H}" fill="url(#bg{uid})"/>\n'
    s += f'  <rect width="{W}" height="{H}" fill="url(#glow{uid})"/>\n'
    shelves = [430, 780, 1120]
    cols = [
        [("#E4D3BC", 78, 150), ("#C9A981", 58, 110), ("#EDE0CC", 66, 128)],
        [("#D9BFA2", 66, 122), ("#EFE3D2", 84, 158), ("#C08A4E", 52, 96)],
        [("#EADCC8", 60, 116), ("#D3B28C", 74, 140), ("#E7D3CB", 62, 120)],
    ]
    for si, y in enumerate(shelves):
        xs = [230, 500, 770]
        for xi, cx in enumerate(xs):
            col, w, h = cols[si][xi]
            s += shadow(uid, cx, y - 4, w * 1.2, 14, ".18")
            s += f'  <rect x="{cx-w}" y="{y-h}" width="{2*w}" height="{h}" rx="12" fill="{col}"/>\n'
            s += f'  <rect x="{cx-w}" y="{y-h}" width="{2*w}" height="{h}" rx="12" fill="url(#rim{uid})"/>\n'
            s += f'  <ellipse cx="{cx}" cy="{y-h}" rx="{w}" ry="{w*.26:.0f}" fill="#fff" opacity=".22"/>\n'
        s += f'  <rect x="60" y="{y}" width="{W-120}" height="12" rx="3" fill="#B99B76" opacity=".55"/>\n'
        s += f'  <rect x="60" y="{y+12}" width="{W-120}" height="10" fill="#000" opacity=".10"/>\n'
    s += grain(uid, W, H, ".08")
    return svg(W, H, s)


def rituale():
    """Macro della fiamma: buio caldo e un solo punto di luce."""
    uid, W, H = 23, 1000, 1250
    s = defs(uid, "#1A1310", "#33241B", "#F2B764", gx="50%", gy="46%", gr="46%")
    s += f'  <rect width="{W}" height="{H}" fill="url(#bg{uid})"/>\n'
    s += f'  <rect width="{W}" height="{H}" fill="url(#glow{uid})"/>\n'
    s += shadow(uid, 500, 950, 260, 32, ".45")
    s += f'  <rect x="0" y="948" width="{W}" height="{H-948}" fill="#0F0A07" opacity=".5"/>\n'
    s += pillar(uid, 500, 600, 954, 150, "#EBDAC2")
    s += f'  <ellipse cx="500" cy="470" rx="330" ry="300" fill="url(#fl{uid})" opacity=".28"/>\n'
    s += f'  <rect width="{W}" height="{H}" fill="url(#vig{uid})"/>\n'
    s += grain(uid, W, H, ".07")
    return svg(W, H, s)


def materia():
    """Strati di cera: campionario di colori colati."""
    uid, W, H = 24, 1000, 1250
    s = defs(uid, "#F7F1E8", "#E6D9C8", "#F6E0BB", gx="42%", gy="30%", gr="70%")
    s += f'  <rect width="{W}" height="{H}" fill="url(#bg{uid})"/>\n'
    s += f'  <rect width="{W}" height="{H}" fill="url(#glow{uid})"/>\n'
    bands = ["#EFE3D2", "#E2CBB0", "#C9A981", "#D9BFA2", "#B98A7D", "#E7D3CB", "#A8834E"]
    y = 130
    for i, c in enumerate(bands):
        h = 100 + (i % 3) * 34
        s += f'  <rect x="{90 + (i%2)*26}" y="{y}" width="{W-180-(i%2)*40}" height="{h}" rx="6" fill="{c}"/>\n'
        s += f'  <rect x="{90 + (i%2)*26}" y="{y}" width="{W-180-(i%2)*40}" height="{h}" rx="6" fill="url(#rim{uid})"/>\n'
        y += h + 12
    s += grain(uid, W, H, ".09")
    return svg(W, H, s)


def sumisura():
    """Coppia di pezzi su misura, formato largo."""
    uid, W, H = 25, 1400, 900
    line = 660
    s = defs(uid, "#1B1512", "#33251B", "#E6AC63", gx="55%", gy="44%", gr="58%")
    s += f'  <rect width="{W}" height="{H}" fill="url(#bg{uid})"/>\n'
    s += f'  <rect width="{W}" height="{H}" fill="url(#glow{uid})"/>\n'
    s += f'  <rect x="0" y="{line}" width="{W}" height="{H-line}" fill="#100B08" opacity=".55"/>\n'
    s += f'  <line x1="0" y1="{line}" x2="{W}" y2="{line}" stroke="#E0A65C" stroke-opacity=".16" stroke-width="2"/>\n'
    for cx, rx in ((470, 180), (760, 110), (990, 140)):
        s += shadow(uid, cx, line + 16, rx, 20, ".42")
    s += pillar(uid, 470, 330, line + 4, 88, "#EFE3D2")
    s += taper(uid, 760, 250, line + 2, 18, "#C9A981")
    s += pillar(uid, 990, 420, line + 4, 66, "#D9BFA2", ribs=False)
    s += f'  <rect width="{W}" height="{H}" fill="url(#vig{uid})"/>\n'
    s += grain(uid, W, H, ".07")
    return svg(W, H, s)


FILES = {"hero.svg": hero, "atelier.svg": atelier, "rituale.svg": rituale,
         "materia.svg": materia, "su-misura.svg": sumisura}

for name, fn in FILES.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(fn())
    print("ok", name)
