#!/usr/bin/env python3
"""Generate 32x32 1-bit home-screen icons for CyberMeow / CapibaraZero.

Outputs an Adafruit_GFX-compatible C header (MSB-first, white = set bit),
a montage PNG of the glyphs, and a composited home-screen preview.
"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 8                      # supersample factor
N = 32                     # final icon size
C = N * S                  # canvas size (256)
FG, BG = 255, 0
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def canvas():
    img = Image.new("L", (C, C), BG)
    return img, ImageDraw.Draw(img)


def arcs_wifi(d, cx, cy, widths, r0, step, a0=215, a1=325, w=20):
    for i in range(widths):
        r = r0 + i * step
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=FG, width=w)


def icon_wifi():
    img, d = canvas()
    cx, cy = C // 2, int(C * 0.74)
    arcs_wifi(d, cx, cy, 3, 46, 46, w=20)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=FG)
    return img


def icon_ble():
    img, d = canvas()
    cx = C // 2
    yt, yb = int(C * 0.10), int(C * 0.90)
    ym = (yt + yb) // 2
    xr, xl = int(C * 0.72), int(C * 0.28)
    yu, yl = int(C * 0.31), int(C * 0.69)
    w = 20
    d.line([(cx, yt), (cx, yb)], fill=FG, width=w)           # spine
    d.line([(cx, yt), (xr, yu), (cx, ym)], fill=FG, width=w, joint="curve")
    d.line([(cx, ym), (xr, yl), (cx, yb)], fill=FG, width=w, joint="curve")
    d.line([(xl, yu), (cx, ym)], fill=FG, width=w)
    d.line([(xl, yl), (cx, ym)], fill=FG, width=w)
    return img


def icon_usb():
    img, d = canvas()
    cx = C // 2
    yt, yb = int(C * 0.08), int(C * 0.92)
    w = 18
    d.line([(cx, yt + 10), (cx, yb)], fill=FG, width=w)       # spine
    # top arrow head
    d.polygon([(cx, yt), (cx - 24, yt + 34), (cx + 24, yt + 34)], fill=FG)
    # left branch -> filled circle
    ylb = int(C * 0.40)
    d.line([(cx, ylb), (int(C * 0.26), ylb - 44)], fill=FG, width=w)
    d.ellipse([int(C * 0.26) - 22, ylb - 44 - 22,
               int(C * 0.26) + 22, ylb - 44 + 22], fill=FG)
    # right branch -> filled square
    yrb = int(C * 0.55)
    d.line([(cx, yrb), (int(C * 0.74), yrb - 44)], fill=FG, width=w)
    s = 22
    d.rectangle([int(C * 0.74) - s, yrb - 44 - s,
                 int(C * 0.74) + s, yrb - 44 + s], fill=FG)
    # base circle
    d.ellipse([cx - 20, yb - 20, cx + 20, yb + 20], fill=FG)
    return img


def icon_subghz():
    img, d = canvas()
    cx = C // 2
    top, bot = int(C * 0.30), int(C * 0.92)
    half = int(C * 0.17)
    w = 18
    d.line([(cx, top), (cx - half, bot)], fill=FG, width=w)   # left leg
    d.line([(cx, top), (cx + half, bot)], fill=FG, width=w)   # right leg
    d.line([(cx - half // 2, (top + bot) // 2),
            (cx + half // 2, (top + bot) // 2)], fill=FG, width=w)  # crossbar
    # radiating arcs at the top
    for r, wd in [(40, 16), (74, 14)]:
        d.arc([cx - r, top - r, cx + r, top + r], 200, 250, fill=FG, width=wd)
        d.arc([cx - r, top - r, cx + r, top + r], 290, 340, fill=FG, width=wd)
    d.ellipse([cx - 12, top - 12, cx + 12, top + 12], fill=FG)
    return img


def icon_nfc():
    img, d = canvas()
    # card outline
    d.rounded_rectangle([int(C * 0.14), int(C * 0.24),
                         int(C * 0.60), int(C * 0.80)], radius=18,
                        outline=FG, width=16)
    # contactless waves opening right
    cx, cy = int(C * 0.52), C // 2
    for r, wd in [(34, 14), (62, 14), (90, 14)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], -45, 45, fill=FG, width=wd)
    return img


def icon_ir():
    img, d = canvas()
    # remote body
    d.rounded_rectangle([int(C * 0.30), int(C * 0.34),
                         int(C * 0.62), int(C * 0.92)], radius=20,
                        outline=FG, width=16)
    d.ellipse([int(C * 0.41), int(C * 0.46), int(C * 0.51), int(C * 0.56)],
              fill=FG)  # button
    # IR beams from top of remote
    cx, cy = int(C * 0.46), int(C * 0.30)
    for r, wd in [(36, 13), (64, 13)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], 250, 290, fill=FG, width=wd)
    return img


def icon_js():
    img, d = canvas()
    try:
        font = ImageFont.truetype(FONT_BOLD, int(C * 0.62))
    except Exception:
        font = ImageFont.load_default()
    text = "JS"
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((C - tw) / 2 - bb[0], (C - th) / 2 - bb[1]), text, fill=FG, font=font)
    return img


def icon_settings():
    img, d = canvas()
    cx = cy = C // 2
    r_out, r_in = int(C * 0.34), int(C * 0.20)
    teeth = 8
    tooth_w = int(C * 0.11)
    tooth_l = int(C * 0.12)
    for k in range(teeth):
        a = math.radians(k * (360 / teeth))
        tx, ty = cx + math.cos(a) * r_out, cy + math.sin(a) * r_out
        # rectangle tooth oriented along the radius (approx with rotated poly)
        dx, dy = math.cos(a), math.sin(a)
        px, py = -dy, dx
        hw = tooth_w / 2
        pts = [
            (tx - px * hw, ty - py * hw),
            (tx + px * hw, ty + py * hw),
            (tx + px * hw + dx * tooth_l, ty + py * hw + dy * tooth_l),
            (tx - px * hw + dx * tooth_l, ty - py * hw + dy * tooth_l),
        ]
        d.polygon(pts, fill=FG)
    d.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], fill=FG)
    d.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], fill=BG)
    return img


ICONS = [
    ("wifi", icon_wifi),
    ("ble", icon_ble),
    ("badusb", icon_usb),
    ("subghz", icon_subghz),
    ("nfc", icon_nfc),
    ("ir", icon_ir),
    ("js", icon_js),
    ("settings", icon_settings),
]


def to_1bit(img):
    small = img.resize((N, N), Image.LANCZOS)
    return small.point(lambda p: 255 if p >= 110 else 0, mode="L")


def pack_msb(img):
    bytew = (N + 7) // 8
    data = bytearray(bytew * N)
    px = img.load()
    for y in range(N):
        for x in range(N):
            if px[x, y] >= 128:
                data[y * bytew + (x >> 3)] |= (0x80 >> (x & 7))
    return data


def main():
    header = []
    header.append("// Auto-generated by tools/gen_icons.py - CyberMeow home icons")
    header.append("// 32x32, 1-bit, MSB-first (Adafruit_GFX drawBitmap format).")
    header.append('#include "Arduino.h"')
    header.append("")
    header.append("#ifndef HOME_ICONS_H")
    header.append("#define HOME_ICONS_H")
    header.append("")
    header.append("#define HOME_ICON_W 32")
    header.append("#define HOME_ICON_H 32")
    header.append("")

    bits = {}
    for name, fn in ICONS:
        b = to_1bit(fn())
        bits[name] = b
        data = pack_msb(b)
        rows = ", ".join("0x%02x" % v for v in data)
        header.append("const uint8_t icon_%s[] = {" % name)
        # wrap at 12 bytes/line
        vals = ["0x%02x" % v for v in data]
        for i in range(0, len(vals), 12):
            header.append("    " + ", ".join(vals[i:i + 12]) + ",")
        header.append("};")
        header.append("")
    header.append("#endif")

    out_h = "include/icons/home/home_icons.h"
    import os
    os.makedirs("include/icons/home", exist_ok=True)
    with open(out_h, "w") as f:
        f.write("\n".join(header))
    print("wrote", out_h)

    # montage of glyphs (upscaled, white on dark)
    pad, cell = 10, 96
    mw = pad + len(ICONS) * (cell + pad)
    mont = Image.new("RGB", (mw, cell + 2 * pad + 24), (12, 15, 20))
    md = ImageDraw.Draw(mont)
    try:
        lf = ImageFont.truetype(FONT_BOLD, 16)
    except Exception:
        lf = ImageFont.load_default()
    for i, (name, _) in enumerate(ICONS):
        big = bits[name].resize((cell, cell), Image.NEAREST)
        tile = Image.new("RGB", (cell, cell), (10, 184, 208))  # teal tile
        glyph = Image.new("RGB", (cell, cell), (255, 255, 255))
        tile.paste(glyph, (0, 0), big)  # white where bit set
        x = pad + i * (cell + pad)
        mont.paste(tile, (x, pad))
        md.text((x + 4, cell + pad + 2), name, fill=(200, 210, 220), font=lf)
    mont.save("tools/icons_montage.png")
    print("wrote tools/icons_montage.png")


if __name__ == "__main__":
    main()
